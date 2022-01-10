from typing import Optional
from fastapi import  Request
from pydantic import BaseModel, Field
from .interest import InterestSchema, InterestModel
from bson import ObjectId


class FocusSchema(BaseModel):
    
    name: str = Field(...)
    interest: str = Field(...)

class FocusModel(BaseModel):
    interest: str
    name: InterestModel


class UpdateFocusModel(BaseModel):
    interest: Optional[str]
    name: Optional[InterestModel]



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