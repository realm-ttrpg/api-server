"""HTTP request/response schema for authz/authn routes"""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    user_id: str
    token: str


class LoginResponse(BaseModel):
    class User(BaseModel):
        id: str
        name: str
        avatar: str

    token: str
    user: User


class SharedGuildsResponse(BaseModel):
    guilds: list[dict]
