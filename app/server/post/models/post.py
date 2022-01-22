from typing import Optional
from fastapi import  Request, File
from pydantic import BaseModel, Field
import  json 
from datetime import datetime
from ...base.models import PaginatedResponseModel, ResponseModel, ErrorResponseModel

class PostSchema(BaseModel):
    
    active_status: Optional[bool] = True
    created_by: Optional[str] = 'admin'
    created_at: datetime = datetime.now()
    updated_by: Optional[str] = 'admin'
    updated_at: datetime = datetime.now()
    is_approved: Optional[bool] = False
    title: str = Field(...)
    event: Optional[str] = None
    content: str = Field(...)
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
    created_at: datetime = datetime.now()
    updated_by: str = Field(...)
    updated_at: datetime = datetime.now()
    is_approved: Optional[bool] = False
    title: str = Field(...)
    event: Optional[str] = None
    content: str = Field(...)
    interest: str = Field(...)
    focus: str = Field(...)
    posted_by: str = Field(...)
    image_file: Optional[str] = None
    attachment_file: Optional[str] = None
    total_likes: Optional[str] = None
    total_comments: Optional[str] = None


class UpdatePostModel(BaseModel):
    active_status: Optional[bool]
    updated_by: Optional[str]
    updated_at: datetime = datetime.now()
    is_approved: Optional[bool] 
    title: Optional[str] 
    event: Optional[str]
    content: Optional[str]
    interest: Optional[str] 
    focus: Optional[str] 
    posted_by: Optional[str] 
    image_file: Optional[str]
    attachment_file: Optional[str]
    total_likes: Optional[str]
    total_comments: Optional[str] 


    class Config:
        arbitrary_types_allowed = True
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value