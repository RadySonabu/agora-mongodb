from fastapi_users import models
from fastapi import  Request
from typing import Optional

class User(models.BaseUser):
    first_name: str
    last_name: str
    profile_pic: Optional[str] = "https://staticfiles-ardy.s3.amazonaws.com/static/default-image.png"


class UserCreate(models.BaseUserCreate):
    first_name: str
    last_name: str
    profile_pic: Optional[str] = "https://staticfiles-ardy.s3.amazonaws.com/static/default-image.png"


class UserUpdate(models.BaseUserUpdate):
    first_name: Optional[str]
    last_name: Optional[str]
    profile_pic: Optional[str] = "https://staticfiles-ardy.s3.amazonaws.com/static/default-image.png"


class UserDB(User, models.BaseUserDB):
    pass

def PaginatedResponseModel(data, message, count, offset, limit, request: Request ):
    client_host = request.client.host
    
    if offset is 0:
        prev_page = None
    else:
        prev_page = f'{client_host}/?offset={offset}&limit={limit}'

    if int(count) > limit:
        next_page = f'{client_host}/?offset={offset}&limit={limit}'
    else:
        next_page =None
    return {
        "count": count,
        "prev": prev_page,
        "next": next_page,
        "results": data,
    }