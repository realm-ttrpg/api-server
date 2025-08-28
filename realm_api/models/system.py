"""Game system model"""

# stdlib
from typing import TYPE_CHECKING

# 3rd party
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .game import Game


class System(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=128)
    slug: str = Field(max_length=16, unique=True)
    games: list["Game"] = Relationship(back_populates="system")
