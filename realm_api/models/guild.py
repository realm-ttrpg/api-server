"""Discord Guild model"""

# 3rd party
from sqlmodel import Field, Relationship, SQLModel

# local
from .game import Game


class Guild(SQLModel, table=True):
    id: str = Field(primary_key=True, max_length=32)
    games: list[Game] = Relationship(back_populates="guild")
