from pydantic import BaseModel


class LoginRequest(BaseModel):
    user_id: str
    token: str


class LoginResponse(BaseModel):
    token: str


class SharedGuildsRequest(BaseModel):
    guild_ids: set[int]


class SharedGuildsResponse(BaseModel):
    guild_ids: set[int]
