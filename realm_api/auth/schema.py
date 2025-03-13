"""HTTP request/response schema for authz/authn routes"""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    user_id: str
    token: str


class LoginResponse(BaseModel):
    token: str


class SharedGuildsResponse(BaseModel):
    guilds: list[dict]
