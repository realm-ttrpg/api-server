"""HTTP request/response schema for authz/authn routes"""

from pydantic import BaseModel


class LoginRequest(BaseModel):
    user_id: str
    token: str


class LoginResponse(BaseModel):
    token: str


class SharedGuildsRequest(BaseModel):
    guild_ids: set[str]


class SharedGuildsResponse(BaseModel):
    guild_ids: set[str]
