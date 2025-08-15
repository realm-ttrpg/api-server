"""Player model"""

# 3rd party
from sqlmodel import Field, Relationship, SQLModel

# local
from .game import Game


class Player(SQLModel, table=True):
    user_id: str = Field(primary_key=True, max_length=32)
    name: str = Field(max_length=32)
    games: list[Game] = Relationship(
        back_populates="players",
        sa_relationship_kwargs={
            "primaryjoin": "Player.user_id == GamePlayer.player_id",
            "secondaryjoin": "GamePlayer.game_id == Game.id",
        },
    )
