from fastapi import APIRouter, Body, Depends, Request, File, UploadFile
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from ..models.post import (
    PostSchema,
    PostModel,
    ResponseModel, 
    ErrorResponseModel,
    PaginatedResponseModel,
    UpdatePostModel, 
    LikePostSchema
)
from ...db import Mongo, post_collection, interest_collection, focus_collection, comment_collection, post_likes_collection
from ...auth.db import user_collection
from typing import Optional
import boto3
from bson import ObjectId
object_name = "Post"
schema = PostSchema
router = APIRouter()

def helper(data) -> dict:
    print(data)

    id_value = str(data['_id'])
    old_key = "_id"
    data.pop(old_key)
    new_dict = {'id': id_value} 
    data = {**new_dict, **data}
    
    return data

db = Mongo(post_collection, helper)

@router.post("/", response_description=f"{object_name} data added into the database")
async def add_data(data: schema = Body(...), image_file: Optional[UploadFile] = File(None), attachment_file: Optional[UploadFile] = File(None)):
    data = jsonable_encoder(data)
    interest_detail = await interest_collection.find_one({'_id': ObjectId(data['interest'])})
    focus_detail = await focus_collection.find_one({'_id': ObjectId(data['focus'])})
    posted_by_detail = await user_collection.find_one({'_id': ObjectId(data['posted_by'])})

    data['interest'] = {
            'id': str(interest_detail['_id']),
            'name': interest_detail['name']
        }
   
    data['focus'] = {
        'id': str(focus_detail['_id']),
        'name': focus_detail['name'],
        'interest': data['interest']
    }

    data['posted_by'] = {
        'id': str(posted_by_detail['_id']),
        'email': posted_by_detail['email'],
        'first_name': posted_by_detail['first_name'],
        'last_name': posted_by_detail['last_name'],
        'profile_pic': posted_by_detail['profile_pic'],
    }

    #Files
    s3_client = boto3.client('s3')
    bucket = 'staticfiles-ardy'

    if image_file:
        filename = image_file.filename
        object_pathname = f'media/{filename}'
        response = s3_client.upload_fileobj(image_file.file, bucket, object_pathname)
        s3_file_path = f'https://{bucket}.s3.amazonaws.com/{object_pathname}'
        data['image_file'] = s3_file_path
    if attachment_file:
        filename = image_file.filename
        object_pathname = f'media/{filename}'
        response = s3_client.upload_fileobj(attachment_file.file, bucket, object_pathname)
        s3_file_path = f'https://{bucket}.s3.amazonaws.com/{object_pathname}'
        data['attachment_file'] = s3_file_path

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
async def update_data(id: str, req: UpdatePostModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_data = await db.update(id, req)
    if updated_data:
        return ResponseModel(
            f"{object_name} with ID: {id} name update is successful"
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
            f"{object_name} with ID: {id} removed", "success"
        )
    return ErrorResponseModel(
        "An error occurred", 404, f"{object_name} with id {0} doesn't exist".format(id)
    )


@router.post("/follow", response_description=f"{object_name} data liked from the database")
async def follow_post(data: LikePostSchema = Body(...)):
    data = jsonable_encoder(data)
    is_liked = await post_likes_collection.find_one({"post": data['post'], "user": data['user']})
    if is_liked:
        return ErrorResponseModel("Post already liked", 422, f"{object_name} with id {is_liked['post']} already liked")
    insert_data = await post_likes_collection.insert_one(data)
    new_data = await post_likes_collection.find_one({"_id": insert_data.inserted_id})

    return ResponseModel(helper(new_data), f"Successfully liked a {object_name}.")

@router.post("/unfollow", response_description=f"{object_name} data liked from the database")
async def unfollow_post(data: LikePostSchema = Body(...)):
    data = jsonable_encoder(data)
    is_liked = await post_likes_collection.find_one({"post": data['post'], "user": data['user']})
    if is_liked:
        await post_likes_collection.delete_one({"_id": ObjectId(is_liked['_id'])})
        return ResponseModel(
            f"{object_name} like with ID: {id} was removed" 
        )
    return ErrorResponseModel(
        "An error occurred", 404, f"{object_name} doesn't exist"
    )