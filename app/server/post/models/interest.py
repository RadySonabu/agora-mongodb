from typing import Optional
from fastapi import  Request
from pydantic import BaseModel, Field
from ...base.models import PaginatedResponseModel, ResponseModel, ErrorResponseModel

class InterestSchema(BaseModel):
    
    name: str = Field(...)
    

class InterestModel(BaseModel):
    name: str


class UpdateInterestModel(BaseModel):
    name: Optional[str]


