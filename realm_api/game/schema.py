"""HTTP request/response schema for game routes"""

from pydantic import BaseModel


class GameResponse(BaseModel):
    id: int
    name: str
