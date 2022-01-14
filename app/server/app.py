import logging
import os
from typing import List
import json
import boto3
import shutil
from botocore.exceptions import ClientError
from fastapi import FastAPI, File, Request, UploadFile, Body

from .post.routes.comment import router as CommentRouter
from .post.routes.focus import router as FocusRouter, focus_collection
from .post.routes.interest import router as InterestRouter
from .post.routes.post import router as PostRouter
from .event.routes.tags import router as TagRouter
from .event.routes.events import router as EventRouter

from .auth.routes import router as UserRouter
from .auth.users import auth_backend, current_active_user, fastapi_users
from pydantic import BaseModel, Field

app = FastAPI()

app.include_router(UserRouter, tags=["users"], prefix="/users")
app.include_router(InterestRouter, tags=["interests"], prefix="/interests")
app.include_router(FocusRouter, tags=["focus"], prefix="/focus")
app.include_router(PostRouter, tags=["posts"], prefix="/posts")
app.include_router(CommentRouter, tags=["comments"], prefix="/comments")
app.include_router(TagRouter, tags=["tags"], prefix="/tags")
app.include_router(EventRouter, tags=["events"], prefix="/events")

app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(fastapi_users.get_register_router(), prefix="/auth", tags=["auth"])
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"],)
app.include_router(fastapi_users.get_verify_router(), prefix="/auth", tags=["auth"],)
app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

@app.get("/root/asd", tags=["Root"])
async def read_root(request: Request):
    info = str(request.url)
    info.rsplit('/',1)
    client_host = request.client.host
    return {"message": f"Welcome to this fantastic app! {info}"}

class UploadModel(BaseModel):
    uploader: str = Field(...)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

@app.post("/uploadfiles/")
async def create_upload_files(file: UploadFile = File(...)):
    filename = file.filename
    bucket = 'staticfiles-ardy'
    object_name = f'ardy/{filename}'
    s3_client = boto3.client('s3')
    response = s3_client.upload_fileobj(file.file, bucket, object_name)

    return filename