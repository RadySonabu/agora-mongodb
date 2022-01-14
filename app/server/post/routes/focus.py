from fastapi import APIRouter, Body, Depends, Request
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from ..models.focus import (
    FocusSchema,
    FocusModel,
    ResponseModel, 
    ErrorResponseModel,
    PaginatedResponseModel,
    UpdateFocusModel
)
from ...db import Mongo, focus_collection, interest_collection, post_collection
from ...auth.db import user_collection
object_name = "Focus"
model_name = 'focus'
schema = FocusSchema
router = APIRouter()

def helper(data) -> dict:
    id_value = str(data['_id'])
    old_key = "_id"
    data.pop(old_key)
    new_dict = {'id': id_value} 
    data = {**new_dict, **data}
    
    return data

db = Mongo(focus_collection, helper)

@router.post("/", response_description=f"{object_name} data added into the database")
async def add_data(data: schema = Body(...)):
    data = jsonable_encoder(data)
    interest_item = await interest_collection.find_one({'_id': ObjectId(data['interest'])})

    data['interest'] = {
        'id': str(interest_item['_id']),
        'name': interest_item['name']
    }
    new_data = await db.add(data)

    return ResponseModel(new_data, f"{object_name} added successfully.")

@router.get("/", response_description=f"{object_name} retrieved", )
async def get_data(limit: int = 10, offset:int=0, request: Request = any):
    query = {}
    queries = request.query_params
    
    for item in queries:
        if item != "limit" and item != "offset":
            query.update({item: queries[item]})
    data = await db.get(limit, offset, query)
    if data:
        return PaginatedResponseModel(data=data['data'], request=request, count=data['count'], offset=offset, limit=limit, message="data data retrieved successfully")
    return PaginatedResponseModel(data=data['data'], request=request, offset=offset, limit=limit, message="Empty list returned")

@router.get("/{id}", response_description=f"{object_name} data retrieved")
async def get_data(id):
    data = await db.retrieve(id)
    if data:
        return ResponseModel(data, f"{object_name} data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, f"{object_name} doesn't exist.")

@router.put("/{id}")
async def update_data(id: str, req: UpdateFocusModel = Body(...)):
    req = {'data':{'update_one':{k: v},'update_many':{f'{model_name}.{k}': v}} for k, v in req.dict().items() if v is not None}
    collection_to_be_updated=[post_collection]
    updated_data = await db.update(id,req, model_name=model_name, collection_to_be_updated=collection_to_be_updated)
    if updated_data:
        return ResponseModel(
            f"{object_name} with ID: {id} name update is successful", 'success'
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        f"There was an error updating the {object_name} data.",
    )

@router.delete("/{id}", response_description=f"{object_name} data deleted from the database")
async def delete_data(id: str):
    deleted_data = await db.delete(id)
    if deleted_data:
        return ResponseModel(
            f"{object_name} with ID: {id} removed" 
        )
    return ErrorResponseModel(
        "An error occurred", 404, f"{object_name} with id {0} doesn't exist".format(id)
    )
