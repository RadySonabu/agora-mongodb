from typing import Optional
from fastapi import  Request
from pydantic import BaseModel, Field
from ...base.models import PaginatedResponseModel, ResponseModel, ErrorResponseModel

class TagSchema(BaseModel):
    
    name: str = Field(...)
    

class TagModel(BaseModel):
    name: str


class UpdateTagModel(BaseModel):
    name: Optional[str]


