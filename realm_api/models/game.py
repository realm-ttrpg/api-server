"""Game model"""

# stdlib
from typing import TYPE_CHECKING

# 3rd party
from sqlmodel import Field, Relationship, SQLModel

# local
from .system import System

if TYPE_CHECKING:
    from .guild import Guild


class Game(SQLModel, table=True):
    id: int = Field(primary_key=True)
    system_id: int = Field(foreign_key="system.id")
    system: System = Relationship(back_populates="games")
    guild_id: str = Field(foreign_key="guild.id")
    guild: "Guild" = Relationship(back_populates="games")
    name: str = Field(max_length=128)
