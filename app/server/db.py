from gc import collect
from typing import List
import motor.motor_asyncio
from bson.objectid import ObjectId
# from fastapi_users.db import MongoDBUserDatabase
# from .auth.users import UserDB
from .auth.db import user_collection
from fastapi import Request, BackgroundTasks
from decouple import config
import time
import concurrent.futures
MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, uuidRepresentation="standard")


interest = client.interests
focus = client.focus
post = client.posts
comment = client.comments
tag = client.tag
event = client.event


interest_collection = interest.get_collection("interest_collection")
focus_collection = focus.get_collection("focus_collection")
post_collection = post.get_collection("post_collection")
post_likes_collection = post.get_collection("post_likes_collection")
comment_collection = comment.get_collection("comment_collection")
comment_likes_collection = post.get_collection("comment_likes_collection")
tag_collection = tag.get_collection("tag_collection")
event_collection = event.get_collection("event_collection")


# Retrieve all students present in the database
class Mongo:
    def __init__(self, collection, helper):
        self.collection = collection
        self.helper = helper

    def count(data):
        data += 1
        return data
    # Get all data
    async def get(self, limit:int, offset:int, query:dict):
        start = time.perf_counter()
        collection = self.collection.find(query)
        
        count = await self.collection.estimated_document_count()
        data = []
        
        async for item in collection.skip(offset).limit(limit):
            data.append(self.helper(item))
        

        end = time.perf_counter()
        print(end-start)
        return {'data': data, 'count': count}

    # Add a new data into to the database
    async def add(self, body: dict) -> dict:
        data = await self.collection.insert_one(body)
        new_data = await self.collection.find_one({"_id": data.inserted_id})
        return self.helper(new_data)

    # Retrieve a data with a matching ID
    async def retrieve(self, id: str) -> dict:
        data = await self.collection.find_one({"_id": ObjectId(id)})
        if data:
            return self.helper(data)


    # Update a data with a matching ID
    async def update(self, id: str,data: dict, model_name, collection_to_be_updated):
        # Return false if an empty request body is sent.
        if len(data) < 1:
            return False
        update_object = await self.collection.find_one({"_id": ObjectId(id)})

        if update_object:
            for item in collection_to_be_updated:
                updated_many = await item.update_many(
                    {f"{model_name}.id": str(update_object['_id'])}, {"$set": data['data']['update_many']}
                )
            updated_one = await self.collection.update_one(
                {"_id": ObjectId(id)}, {"$set": data['data']['update_one']}
            )
            
            if updated_many:
                return True
            return False


    # Delete a data from the database
    async def delete(self, id: str):
        data = await self.collection.find_one({"_id": ObjectId(id)})
        if data:
            await self.collection.delete_one({"_id": ObjectId(id)})
            return True