import os
from fastapi import APIRouter
import motor.motor_asyncio
from fastapi_users.db import MongoDBUserDatabase
from .models import UserDB
from decouple import config

MONGO_DETAILS = config('MONGO_DETAILS')

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_DETAILS, uuidRepresentation="standard"
)
db = client["users"]
user_collection = db.user_collection


async def get_user_db():
    yield MongoDBUserDatabase(UserDB, user_collection)
