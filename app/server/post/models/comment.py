from typing import Optional
from fastapi import  Request
from pydantic import BaseModel, Field
from bson import ObjectId
import datetime
from ...base.models import PaginatedResponseModel, ResponseModel, ErrorResponseModel

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



