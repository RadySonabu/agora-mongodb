import datetime
import email
from fastapi import  Request
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

from ...base.models import PaginatedResponseModel, ResponseModel, ErrorResponseModel

class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    date_joined: Optional[datetime.datetime] = datetime.datetime.now()
    date_of_birth: Optional[datetime.date]
    location: Optional[str]
    role :str
    profile_pic: Optional[str] = "https://staticfiles-ardy.s3.amazonaws.com/static/default-image.png"

class UserLogin(BaseModel):
    email: EmailStr
    password: str   

class UserSchema(BaseModel):
    email: EmailStr
    # password: str
    first_name: str
    last_name: str
    date_joined: Optional[datetime.datetime] = datetime.datetime.now()
    date_of_birth: Optional[datetime.date]
    location: Optional[str]
    role :str
    profile_pic: Optional[str] = "https://staticfiles-ardy.s3.amazonaws.com/static/default-image.png"


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    date_joined: Optional[datetime.datetime] = datetime.datetime.now()
    date_of_birth : Optional[datetime.datetime]
    location : Optional[str]
    role : str
    profile_pic: Optional[str] = "https://staticfiles-ardy.s3.amazonaws.com/static/default-image.png"


class UserUpdateModel(BaseModel):
    # email: EmailStr
    # password: str
    first_name: Optional[str]
    last_name: Optional[str]
    date_joined: Optional[datetime.datetime] = datetime.datetime.now()
    date_of_birth : Optional[datetime.datetime]
    location : Optional[str]
    role : Optional[str]
    profile_pic: Optional[str] = "https://staticfiles-ardy.s3.amazonaws.com/static/default-image.png"


class UserDB(UserSchema):
    pass

class UserChangePassword(BaseModel):
    new_password: str
    confirm_new_password: str
    old_password: str