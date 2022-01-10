from fastapi import APIRouter, Body, Depends, Request
from fastapi.encoders import jsonable_encoder
from .models import PaginatedResponseModel

from ..db import Mongo
from .db import user_collection

object_name = "User"
router = APIRouter()

def user_helper(data) -> dict:
    return {
        "id": str(data['_id']),
        "uuid": str(data['id']),
        "email": data['email'],
        "is_active": data['is_active'],
        "is_superuser": data['is_superuser'],
        "is_verified": data['is_verified'],
        "first_name": data['first_name'],
        "last_name": data['last_name'],
        "profile_pic": data['profile_pic']
    }
db = Mongo(user_collection, user_helper)

@router.get("/", response_description=f"{object_name} retrieved", )
async def get_classrooms(limit: int = 10, offset:int=0, request: Request = any):
    query = {}
    queries = request.query_params
    
    for item in queries:
        if item != "limit" and item != "offset":
            query.update({item: queries[item]})
    users = await db.get(limit, offset, query)
    if users:
        return PaginatedResponseModel(data=users['data'], request=request, count=users['count'], offset=offset, limit=limit, message="user data retrieved successfully")
    return PaginatedResponseModel(data=users['data'], request=request, offset=offset, limit=limit, message="Empty list returned")