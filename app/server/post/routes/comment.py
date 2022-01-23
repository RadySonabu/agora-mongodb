from fastapi import APIRouter, Body, Depends, Request
from fastapi.encoders import jsonable_encoder
from bson import ObjectId
from ..models.comment import (
    CommentSchema,
    CommentModel,
    ResponseModel, 
    ErrorResponseModel,
    PaginatedResponseModel,
    UpdateCommentModel,
    LikeCommentSchema
)
from ...db import Mongo, post_collection, interest_collection, focus_collection, comment_collection, comment_likes_collection
from ...auth.db import user_collection
object_name = "Comment"
schema = CommentSchema
router = APIRouter()

def helper(data) -> dict:
    id_value = str(data['_id'])
    old_key = "_id"
    data.pop(old_key)
    new_dict = {'id': id_value} 
    data = {**new_dict, **data}
    
    return data

db = Mongo(comment_collection, helper)

@router.post("/", response_description=f"{object_name} data added into the database")
async def add_data(data: schema = Body(...)):
    data = jsonable_encoder(data)
    author_detail = await user_collection.find_one({'_id': ObjectId(data['author'])})
    post_detail = await post_collection.find_one({'_id': ObjectId(data['post'])})
    
    data['post'] = {
            'id': str(post_detail['_id']),
            'title': post_detail['title']

        }

    data['author'] = {
        'id': str(author_detail['_id']),
        'email': author_detail['email'],
        'first_name': author_detail['first_name'],
        'last_name': author_detail['last_name'],
        'profile_pic': author_detail['profile_pic'],
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
async def update_data(id: str, req: UpdateCommentModel = Body(...)):
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
            f"{object_name} with ID: {id} removed" 
        )
    return ErrorResponseModel(
        "An error occurred", 404, f"{object_name} with id {0} doesn't exist".format(id)
    )


@router.post("/like", response_description=f"{object_name} data liked from the database")
async def like_comment(data: LikeCommentSchema = Body(...)):
    data = jsonable_encoder(data)
    is_liked = await comment_likes_collection.find_one({"comment": data['comment'], "user": data['user']})
    if is_liked:
        return ErrorResponseModel("Comment already liked", 422, f"{object_name} with id {is_liked['post']} already liked")
    insert_data = await comment_likes_collection.insert_one(data)
    new_data = await comment_likes_collection.find_one({"_id": insert_data.inserted_id})

    return ResponseModel(helper(new_data), f"Successfully liked a {object_name}.")

@router.post("/dislike", response_description=f"{object_name} data liked from the database")
async def dislike_comment(data: LikeCommentSchema = Body(...)):
    data = jsonable_encoder(data)
    is_liked = await comment_likes_collection.find_one({"comment": data['comment'], "user": data['user']})
    if is_liked:
        await comment_likes_collection.delete_one({"_id": ObjectId(is_liked['_id'])})
        return ResponseModel(
            f"{object_name} like with ID: {id} was removed" 
        )
    return ErrorResponseModel(
        "An error occurred", 404, f"{object_name} doesn't exist"
    )