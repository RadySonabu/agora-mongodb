import motor.motor_asyncio
from bson.objectid import ObjectId
from fastapi_users.db import MongoDBUserDatabase
from .auth.users import UserDB
from fastapi import Request
from decouple import config

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
comment_collection = comment.get_collection("comment_collection")
tag_collection = tag.get_collection("tag_collection")
event_collection = event.get_collection("event_collection")


# Retrieve all students present in the database
class Mongo:
    def __init__(self, collection, helper):
        self.collection = collection
        self.helper = helper

    async def get(self, limit:int, offset:int, query:dict):
        collection = self.collection.find(query)
        count = await self.collection.count_documents(query)
        data = []
        async for item in collection.skip(offset).limit(limit):
            data.append(self.helper(item))
        return {'data': data, 'count': count}

    # Add a new student into to the database
    async def add(self, body: dict) -> dict:
        data = await self.collection.insert_one(body)
        new_data = await self.collection.find_one({"_id": data.inserted_id})
        return self.helper(new_data)

    # Retrieve a student with a matching ID
    async def retrieve(self, id: str) -> dict:
        data = await self.collection.find_one({"_id": ObjectId(id)})
        if data:
            return self.helper(data)


    # Update a student with a matching ID
    async def update(self, id: str, data: dict):
        # Return false if an empty request body is sent.
        if len(data) < 1:
            return False
        update_object = await self.collection.find_one({"_id": ObjectId(id)})
        print(update_object)
        if update_object:
            updated_data = await self.collection.update_one(
                {"_id": ObjectId(id)}, {"$set": data}
            )
            
            if updated_data:
                return True
            return False


    # Delete a student from the database
    async def delete(self, id: str):
        student = await self.collection.find_one({"_id": ObjectId(id)})
        if student:
            await self.collection.delete_one({"_id": ObjectId(id)})
            return True