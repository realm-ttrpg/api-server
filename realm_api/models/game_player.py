"""Game Player model"""

# 3rd party
from sqlmodel import Field, SQLModel

# local
from .game import Game
from .player import Player


class GamePlayer(SQLModel, table=True):
    game_id: int = Field(foreign_key=Game.id, primary_key=True)
    player_id: str = Field(foreign_key=Player.user_id, primary_key=True)
