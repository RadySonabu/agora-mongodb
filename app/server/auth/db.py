import os
from fastapi import APIRouter
import motor.motor_asyncio
from fastapi_users.db import MongoDBUserDatabase
from .models import UserDB
MONGO_DETAILS = "mongodb+srv://admin:admin@cluster0.dauoh.mongodb.net/agora?retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(
    MONGO_DETAILS, uuidRepresentation="standard"
)
db = client["users"]
user_collection = db.user_collection


async def get_user_db():
    yield MongoDBUserDatabase(UserDB, user_collection)
