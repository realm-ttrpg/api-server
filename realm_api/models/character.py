"""Character model"""

# 3rd party
from sqlmodel import Field, SQLModel

# local
from .game import Game


class Character(SQLModel, table=True):
    id: int = Field(primary_key=True)
    game_id: int = Field(foreign_key=Game.id)
