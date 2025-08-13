"""Game Role model"""

# 3rd party
from sqlmodel import Field, SQLModel

# local
from .game import Game
from .role import Role


class GameRole(SQLModel, table=True):
    game_id: int = Field(foreign_key=Game.id, primary_key=True)
    role_id: int = Field(foreign_key=Role.id, primary_key=True)
