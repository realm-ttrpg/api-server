"""HTTP request/response schema for game routes"""

# 3rd party
from pydantic import BaseModel


class GameResponse(BaseModel):
    id: int
    name: str
