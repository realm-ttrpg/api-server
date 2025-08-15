"""Role model"""

# stdlib
from typing import TYPE_CHECKING

# 3rd party
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .player import Player


class Role(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=32)
    players: list["Player"] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "Role.id == GamePlayerRole.role_id",
            "secondaryjoin": "GamePlayerRole.id == Player.id",
        }
    )
