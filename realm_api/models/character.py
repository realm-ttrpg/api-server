"""Character model"""

# stdlib
from typing import TYPE_CHECKING

# 3rd party
from sqlmodel import Field, Relationship, SQLModel

# local
from .character_prop import CharacterProp
from .character_stat import CharacterStat
from .game_player_character import GamePlayerCharacter

if TYPE_CHECKING:
    from .game_player import GamePlayer


class Character(SQLModel, table=True):
    id: int = Field(primary_key=True)
    game_id: int = Field(foreign_key="game.id")
    managers: list["GamePlayer"] = Relationship(
        back_populates="characters",
        link_model=GamePlayerCharacter,
        sa_relationship_kwargs={
            "primaryjoin": "Character.id == GamePlayerCharacter.character_id",
            "secondaryjoin": "GamePlayerCharacter.player_id == GamePlayer.player_id",
        },
    )
    props: list[CharacterProp] = Relationship(back_populates="character")
    stats: list[CharacterStat] = Relationship(back_populates="character")
