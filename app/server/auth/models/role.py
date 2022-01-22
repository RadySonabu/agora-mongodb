from typing import Optional
from pydantic import BaseModel
from  ...base.models import PaginatedResponseModel, ResponseModel, ErrorResponseModel

class RoleSchema(BaseModel):
    name: str

class RoleModel(BaseModel):
    name: str

class UpdateRoleModel(BaseModel):
    name: Optional[str]
    


