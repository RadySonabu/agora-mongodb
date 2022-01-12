from typing import Optional
from fastapi import  Request
from pydantic import BaseModel, Field
from .interest import InterestSchema, InterestModel
from bson import ObjectId
from ...base.models import PaginatedResponseModel, ResponseModel, ErrorResponseModel


class FocusSchema(BaseModel):
    
    name: str = Field(...)
    interest: str = Field(...)

class FocusModel(BaseModel):
    interest: str
    name: InterestModel


class UpdateFocusModel(BaseModel):
    interest: Optional[str]
    name: Optional[InterestModel]

