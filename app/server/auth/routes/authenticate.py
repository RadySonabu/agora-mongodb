from datetime import datetime, time, timedelta
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, Request, Response, status
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
import jwt

from ..db import role_collection, user_collection, blacklist_token_collection
from ..models.my_user import (ErrorResponseModel, PaginatedResponseModel,
                              ResponseModel, UserLogin, UserRegistrationSchema,
                              UserSchema, UserUpdateModel)
from ..models.token import Token, RefreshToken

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
router = APIRouter()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(email: EmailStr, password: str):
    user = user_collection.find_one({'email': email})
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def parse_helper(data) -> dict:
    id_value = str(data['_id'])
    old_key = "_id"
    data.pop(old_key)
    new_dict = {'id': id_value} 
    data = {**new_dict, **data}
    return data

def generate_token(data):
    dt = datetime.today()  # Get timezone naive now
    seconds = dt.timestamp()
    exp = datetime.utcnow() + timedelta(minutes=15)
    jti = f"{data['id']}{int(seconds)}"
    access_token_payload = {
        "user_id": data['id'],
        "exp": exp,
        "jti": jti,
        "token_type": 'access'
    }
    refresh_token_payload = {
        "user_id": data['id'],
        "exp": datetime.utcnow() + timedelta(days=1),
        "jti": jti,
        "token_type": 'access'
    }
    access_token = jwt.encode(access_token_payload, SECRET_KEY)
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY)

    return {'access_token': access_token, "refresh_token": refresh_token}

@router.post("/login")
async def login(response: Response, data: UserLogin = Body(...)):
    try:
        user_data = await user_collection.find_one({'email': data.email})
        user = parse_helper(user_data)
        if not user:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'error': 'Incorrect credentials!'}
        
        if not verify_password(data.password, user['password']):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'error': 'Incorrect credentials!'}
        
        token = generate_token(user)
        res = {
            'access_token': token['access_token'],
            'refresh_token': token['refresh_token'],
            "message": "success"
        }

        return res
    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED

@router.post("/logout")
async def logout(request: Request, response: Response):

    # add to db the blacklisted tokens
    try:
        token_value = request.headers['authorization']
        token = token_value.replace("Bearer ","")
        is_blacklisted = await blacklist_token_collection.find_one({'token': token})
        if is_blacklisted:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {
                "detail": "Token is invalid or expired",
                "code": "token_not_valid"
            }
        jwt_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        body = {
            "token": token,
            "exp": jwt_token['exp'],
            "status": "invalid"
        }
        data = await blacklist_token_collection.insert_one(body)
        new_data = await blacklist_token_collection.find_one({"_id": data.inserted_id})
        return parse_helper(new_data)
    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"detail": "Authentication credentials were not provided."}

@router.post("/token")
async def obtain_token(response: Response, data: UserLogin = Body(...)):
    try:
        user_data = await user_collection.find_one({'email': data.email})
        user = parse_helper(user_data)
        if not user:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'error': 'Incorrect credentials!'}
        
        if not verify_password(data.password, user['password']):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {'error': 'Incorrect credentials!'}
        
        token = generate_token(user)
        res = {
            'access_token': token['access_token'],
            'refresh_token': token['refresh_token'],
            "message": "success"
        }

        return res
    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED

@router.post("/token/verify")
async def verify_token(token: Token, response: Response):
    try:
        value = token.token
        is_blacklisted = await blacklist_token_collection.find_one({'token': value})
        if is_blacklisted:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {
                "detail": "Token is invalid or expired",
                "code": "token_not_valid"
            }
        token = jwt.decode(value, SECRET_KEY, algorithms=[ALGORITHM])
    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "detail": "Token is invalid or expired",
            "code": "token_not_valid"
        }
    return {}

@router.post("/token/refresh")
async def refresh_token(token: RefreshToken, response: Response):
    # create a new access token 
    try:
        value = token.refresh
        is_blacklisted = await blacklist_token_collection.find_one({'token': value})
        if is_blacklisted:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {
                "detail": "Token is invalid or expired",
                "code": "token_not_valid"
            }
        jwt_token = jwt.decode(value, SECRET_KEY, algorithms=[ALGORITHM])
        token = generate_token({"id": jwt_token['user_id']})

        return {'access_token': token['access_token'], "token_type": "Bearer"}
    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "detail": "Token is invalid or expired",
            "code": "token_not_valid"
        }
    
@router.post("/token/user-details")
async def user_detail_token(request: Request, response: Response):
    # create a new access token 
    try:
        token_value = request.headers['authorization']
        token = token_value.replace("Bearer ","")
        is_blacklisted = await blacklist_token_collection.find_one({'token': token})
        if is_blacklisted:
            response.status_code = status.HTTP_401_UNAUTHORIZED
            return {
                "detail": "Token is invalid or expired",
                "code": "token_not_valid"
            }
        jwt_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user = await user_collection.find_one({"_id": ObjectId(jwt_token['user_id'])})
        # removes tha hased password to the returned value
        user.pop('password')
        return parse_helper(user)
    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "detail": "Token is invalid or expired",
            "code": "token_not_valid"
        }