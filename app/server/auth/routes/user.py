from datetime import datetime, time, timedelta
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, Request, Response, status
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
import jwt

from ...db import Mongo
from ..db import role_collection, user_collection, blacklist_token_collection
from ..models.my_user import (ErrorResponseModel, PaginatedResponseModel,
                              ResponseModel, UserLogin, UserRegistrationSchema,
                              UserSchema, UserUpdateModel, UserChangePassword)
from ..models.token import Token
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")





object_name = "User"
router = APIRouter()
schema = UserSchema
def user_helper(data) -> dict:
    id_value = str(data['_id'])
    old_key = "_id"
    data.pop(old_key)
    data.pop("password")
    new_dict = {'id': id_value} 
    data = {**new_dict, **data}
    return data
db = Mongo(user_collection, user_helper)
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@router.post("/", response_description=f"{object_name} data added into the database")
async def add_data(data: UserRegistrationSchema = Body(...)):
    data = jsonable_encoder(data)
    role_item = await role_collection.find_one({'_id': ObjectId(data['role'])})
    data['role'] = {
        'id': str(role_item['_id']),
        'name': role_item['name']
    }
    data['password'] = get_password_hash(data['password'])
    new_data = await db.add(data)
    return ResponseModel(new_data, f"{object_name} added successfully.")

@router.get("/", response_description=f"{object_name} retrieved", )
async def get_data(limit: int = 10, offset:int=0, request: Request = any):
    query = {}
    queries = request.query_params
    
    for item in queries:
        if item != "limit" and item != "offset":
            query.update({item: queries[item]})
    users = await db.get(limit, offset, query)
    if users:
        return PaginatedResponseModel(data=users['data'], request=request, count=users['count'], offset=offset, limit=limit, message="user data retrieved successfully")
    return PaginatedResponseModel(data=users['data'], request=request, offset=offset, limit=limit, message="Empty list returned")

@router.get("/{id}", response_description=f"{object_name} data retrieved")
async def get_data(id):
    data = await db.retrieve(id)
    if data:
        return ResponseModel(data, f"{object_name} data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, f"{object_name} doesn't exist.")

@router.put("/{id}")
async def update_data(id: str, req: UserUpdateModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_data = await db.update(id, req)
    if updated_data:
        return ResponseModel(
            f"{object_name} with ID: {id} name update is successful", 'Success'
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        f"There was an error updating the {object_name} data.",
    )

@router.delete("/{id}", response_description=f"{object_name} data deleted from the database")
async def delete_data(id: str):
    deleted_data = await db.delete(id)
    if deleted_data:
        return ResponseModel(
            f"{object_name} with ID: {id} removed" 
        )
    return ErrorResponseModel(
        "An error occurred", 404, f"{object_name} with id {0} doesn't exist".format(id)
    )

@router.put("/password/change")
async def change_password(request: Request, response: Response, data: UserChangePassword = Body(...)):
    try:
        token_value = request.headers['authorization']
        token = token_value.replace("Bearer ","")
        jwt_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user = await user_collection.find_one({'_id': ObjectId(jwt_token['user_id'])})
        new_password = data.new_password
        confirm_new_password = data.confirm_new_password
        old_password = data.old_password
        if new_password != confirm_new_password:
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "detail": "Password does not match"
            }
        if not verify_password(old_password, user['password']):
            response.status_code = status.HTTP_400_BAD_REQUEST
            return {
                "detail": "Invalid Password"
            }
        user = user_helper(user)
        new_user = await user_collection.update_one(
                {"_id": ObjectId(user['id'])}, {"$set": {"password": get_password_hash(new_password)}}
            )
        return {
            "detail": "Password updated"
        }
    except:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {
            "detail": "Token is invalid or expired",
            "code": "token_not_valid"
        }