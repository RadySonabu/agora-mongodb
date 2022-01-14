from typing import Optional

import boto3
from bson import ObjectId
from fastapi import APIRouter, Body, Depends, File, Request, UploadFile
from fastapi.encoders import jsonable_encoder

from ...auth.db import user_collection
from ...db import (Mongo, comment_collection, focus_collection, event_collection,
                   interest_collection, post_collection)
from ..models.events import (ErrorResponseModel, PaginatedResponseModel,
                           EventSchema,  ResponseModel, UpdateEventModel, EventModel
                           )

object_name = "Event"
schema = EventSchema
router = APIRouter()

def helper(data) -> dict:
    id_value = str(data['_id'])
    new_key = "id"
    old_key = "_id"
    data.pop(old_key)
    new_dict = {'id': id_value} 
    data = {**new_dict, **data}
    
    return data

db = Mongo(event_collection, helper)

@router.post("/", response_description=f"{object_name} data added into the database")
async def add_data(data: schema = Body(...), main_event_image: Optional[UploadFile] = File(None)):
    data = jsonable_encoder(data)

    s3_client = boto3.client('s3')
    bucket = 'staticfiles-ardy'

    if main_event_image:
        filename = main_event_image.filename
        object_pathname = f'media/{filename}'
        response = s3_client.upload_fileobj(main_event_image.file, bucket, object_pathname)
        s3_file_path = f'https://{bucket}.s3.amazonaws.com/{object_pathname}'
        data['main_event_image'] = s3_file_path
    
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

    for item in data['data']:
        print(item)
        interest_detail = await interest_collection.find_one({'_id': ObjectId(item['interest'])})
        focus_detail = await focus_collection.find_one({'_id': ObjectId(item['focus'])})
        organizer_detail = await user_collection.find_one({'_id': ObjectId(item['organizer'])})

        item['interest'] = {
            'id': str(interest_detail['_id']),
            'name': interest_detail['name']
        }

        item['focus'] = {
            'id': str(focus_detail['_id']),
            'name': focus_detail['name'],
            'interest': item['interest']
        }

        item['organizer'] = {
            'id': str(organizer_detail['_id']),
            'email': organizer_detail['email'],
            'first_name': organizer_detail['first_name'],
            'last_name': organizer_detail['last_name'],
            'profile_pic': organizer_detail['profile_pic'],
        }
        

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
async def update_data(id: str, req: UpdateEventModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_data = await db.update(id, req)
    if updated_data:
        return ResponseModel(
            f"{object_name} with ID: {id} name update is successful", 'Success'
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
