import json
import os

import boto3
from botocore.exceptions import ClientError
from fastapi import (Body, Depends, FastAPI, File, HTTPException, Request,
                     UploadFile)
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pydantic import BaseModel, Field

# from .auth.models.user import UserDB
from .auth.routes.role import router as RoleRouter
from .auth.routes.user import router as UserRouter
from .auth.routes.user import user_collection
from .auth.routes.authenticate import router as AuthRouter
# from .auth.users import auth_backend, current_active_user, fastapi_users
from .event.routes.events import router as EventRouter
from .event.routes.tags import router as TagRouter
from .post.routes.comment import router as CommentRouter
from .post.routes.focus import focus_collection
from .post.routes.focus import router as FocusRouter
from .post.routes.interest import router as InterestRouter
from .post.routes.post import router as PostRouter

app = FastAPI()


origins = [
    "http://127.0.0.1:8000",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(AuthRouter, tags=["auth"], prefix="")
app.include_router(UserRouter, tags=["users"], prefix="/users")
app.include_router(RoleRouter, tags=["user-role"], prefix="/user-role")
app.include_router(InterestRouter, tags=["interests"], prefix="/base/interests")
app.include_router(FocusRouter, tags=["focus"], prefix="/base/focus")
app.include_router(PostRouter, tags=["posts"], prefix="/posts")
app.include_router(CommentRouter, tags=["comments"], prefix="/comments")
app.include_router(TagRouter, tags=["tags"], prefix="/events/tags")
app.include_router(EventRouter, tags=["events"], prefix="/events/event-registration")

# app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="", tags=["auth"])
# app.include_router(fastapi_users.get_register_router(), prefix="", tags=["auth"])
# app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"],)
# app.include_router(fastapi_users.get_verify_router(), prefix="/auth", tags=["auth"],)
# app.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])

@app.get("/", tags=["Root"])
async def read_root(request: Request):
    client_host = request.client.host
    return {"message": f"Welcome to this fantastic app! "}

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

class UserLogin(BaseModel):
    username: str
    password: str
    
# @app.post('/login')
# async def login(user: UserLogin):
#     user = await user_collection.find_one({'email': user.username})
#     print(user['email'], "this is the username")
#     return 'asdf'
