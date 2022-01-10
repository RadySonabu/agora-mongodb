from typing import Optional
from fastapi import  Request, File
from pydantic import BaseModel, Field
import datetime, json 

class PostSchema(BaseModel):
    
    active_status: Optional[bool] = True
    created_by: Optional[str] = 'admin'
    created_at: Optional[datetime.datetime] = datetime.datetime.now()
    updated_by: Optional[str] = 'admin'
    updated_at: Optional[datetime.datetime] = datetime.datetime.now()
    title: str = Field(...)
    event: Optional[str] = None
    interest: str = Field(...)
    focus: str = Field(...)
    posted_by: str = Field(...)
    image_file: Optional[str] = None
    attachment_file: Optional[str] = None
    total_likes: Optional[str] = "0"
    total_comments: Optional[str] = "0"

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


class PostModel(BaseModel):
    active_status: Optional[bool] = True
    created_by: str = Field(...)
    created_at: datetime.datetime = datetime.datetime.now()
    updated_by: str = Field(...)
    updated_at: datetime.datetime = datetime.datetime.now()
    title: str = Field(...)
    event: Optional[str] = None
    interest: str = Field(...)
    focus: str = Field(...)
    posted_by: str = Field(...)
    image_file: Optional[str] = None
    attachment_file: Optional[str] = None
    total_likes: Optional[str] = None
    total_comments: Optional[str] = None


class UpdatePostModel(BaseModel):
    active_status: Optional[bool] = True
    created_by: Optional[str] 
    created_at: datetime.datetime = datetime.datetime.now()
    updated_by: Optional[str]
    updated_at: datetime.datetime = datetime.datetime.now()
    title: Optional[str] 
    event: Optional[str] 
    interest: Optional[str] 
    focus: Optional[str] 
    posted_by: Optional[str] 
    image_file: Optional[str]
    attachment_file: Optional[str]
    total_likes: Optional[str]
    total_comments: Optional[str] 



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