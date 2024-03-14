from pydantic import BaseModel


class LoginRequest(BaseModel):
    user_id: str
    token: str


class LoginResponse(BaseModel):
    token: str
