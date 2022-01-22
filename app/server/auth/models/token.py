from pydantic import BaseModel


class Token(BaseModel):
    token: str


class RefreshToken(BaseModel):
    refresh: str