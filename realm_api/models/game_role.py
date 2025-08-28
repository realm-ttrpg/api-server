"""Game Role model"""

# 3rd party
from sqlmodel import Field, Relationship, SQLModel

# local
from .game import Game
from .game_player import GamePlayer
from .game_player_role import GamePlayerRole


class GameRole(SQLModel, table=True):
    __tablename__ = "game_role"  # type: ignore

    game_id: int = Field(foreign_key="game.id", primary_key=True)
    game: Game = Relationship()
    role_id: int = Field(foreign_key="role.id", primary_key=True)
    members: list[GamePlayer] = Relationship(
        back_populates="roles",
        link_model=GamePlayerRole,
        sa_relationship_kwargs={
            "primaryjoin": "GameRole.role_id == GamePlayerRole.role_id",
            "secondaryjoin": "GamePlayerRole.player_id == GamePlayer.player_id",
        },
    )
