import datetime
from fastapi_users import models
from fastapi import  Request
from typing import Optional
from pydantic import BaseModel, Field

from ...base.models import PaginatedResponseModel, ResponseModel, ErrorResponseModel

class User(models.BaseUser):
    first_name: str
    last_name: str
    # date_joined: Optional[datetime.datetime] = datetime.datetime.now()
    # date_of_birth = Optional[datetime.datetime]
    # location = Optional[str]
    # role = str
    profile_pic: Optional[str] = "https://staticfiles-ardy.s3.amazonaws.com/static/default-image.png"


class UserCreate(models.BaseUserCreate):
    first_name: str
    last_name: str
    # date_joined: Optional[datetime.datetime] = datetime.datetime.now()
    # date_of_birth = Optional[datetime.datetime]
    # location = Optional[str]
    # role = str
    profile_pic: Optional[str] = "https://staticfiles-ardy.s3.amazonaws.com/static/default-image.png"


class UserUpdate(models.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    # date_joined: Optional[datetime.datetime] = datetime.datetime.now()
    # date_of_birth = Optional[datetime.datetime]
    # location = Optional[str]
    # role = Optional[str]
    profile_pic: Optional[str] = "https://staticfiles-ardy.s3.amazonaws.com/static/default-image.png"


class UserDB(User, models.BaseUserDB):
    pass

