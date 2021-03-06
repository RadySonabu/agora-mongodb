import os
from fastapi import APIRouter
import motor.motor_asyncio
from fastapi_users.db import MongoDBUserDatabase
from .models.user import UserDB
from decouple import config

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_DETAILS, uuidRepresentation="standard"
)
user = client["users"]

user_collection = user.get_collection("user_collection")
role_collection = user.get_collection("role_collection")
blacklist_token_collection = user.get_collection("blacklist_token_collection")

async def get_user_db():
    yield MongoDBUserDatabase(UserDB, user_collection)
