"""Player model"""

# 3rd party
from sqlmodel import Field, Relationship, SQLModel

# local
from .game import Game
from .game_player import GamePlayer


class Player(SQLModel, table=True):
    user_id: str = Field(primary_key=True, max_length=32)
    name: str = Field(max_length=32)
    games: list[Game] = Relationship(
        link_model=GamePlayer,
        sa_relationship_kwargs={
            "primaryjoin": "Player.user_id == GamePlayer.player_id",
            "secondaryjoin": "GamePlayer.game_id == Game.id",
            "overlaps": "game,player,players",
        },
    )
