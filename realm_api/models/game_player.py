"""Game Player model"""

# stdlib
from typing import TYPE_CHECKING

# 3rd party
from sqlmodel import Field, Relationship, SQLModel

# local
from .character import Character
from .game import Game
from .player import Player

if TYPE_CHECKING:
    from .game_role import GameRole


class GamePlayer(SQLModel, table=True):
    __tablename__ = "game_player"  # type: ignore

    game_id: int = Field(foreign_key="game.id", primary_key=True)
    game: Game = Relationship(back_populates="players")
    player_id: str = Field(foreign_key="player.user_id", primary_key=True)
    player: Player = Relationship()
    characters: list[Character] = Relationship(
        back_populates="managers",
        sa_relationship_kwargs={
            "primaryjoin": "GamePlayer.player_id == GamePlayerCharacter.player_id",
            "secondaryjoin": "GamePlayerCharacter.character_id == Character.id",
        },
    )
    roles: list["GameRole"] = Relationship(
        back_populates="members",
        sa_relationship_kwargs={
            "primaryjoin": "GamePlayer.player_id == GamePlayerRole.player_id",
            "secondaryjoin": "GamePlayerRole.role_id == GameRole.role_id",
        },
    )
