from typing import Optional
from fastapi import  Request
from pydantic import BaseModel, Field
from bson import ObjectId
import datetime

class CommentSchema(BaseModel):
    
    active_status: Optional[bool] = True
    created_by: Optional[str] = 'admin'
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_by: Optional[str] = 'admin'
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    post: str = Field(...)
    author: str = Field(...)
    message: str = Field(...)
    parent_id: Optional[str] = None
    total_likes: Optional[str] = "0"


class CommentModel(BaseModel):
    active_status: Optional[bool] = True
    created_by: Optional[str] = 'admin'
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_by: Optional[str] = 'admin'
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    post: str = Field(...)
    author: str = Field(...)
    message: str = Field(...)
    parent_id: Optional[str] = None
    total_likes: Optional[str] = "0"


class UpdateCommentModel(BaseModel):
    active_status: Optional[bool] = True
    created_by: Optional[str] 
    created_at: datetime.datetime = datetime.datetime.now()
    updated_by: Optional[str]
    updated_at: datetime.datetime = datetime.datetime.now()
    post: Optional[str] 
    author: Optional[str] 
    message: Optional[str] 
    parent_id: Optional[str]
    total_likes: Optional[str] 



def PaginatedResponseModel(data, message, count, offset, limit, request: Request ):
    client_host = request.client.host
    
    if offset == 0:
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

def ResponseModel(data, message):
    return data

def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}