"""Character property model"""

# stdlib
from typing import TYPE_CHECKING

# 3rd party
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .character import Character


class CharacterProp(SQLModel, table=True):
    __tablename__ = "character_prop"  # type: ignore

    character_id: int = Field(foreign_key="character.id", primary_key=True)
    character: "Character" = Relationship(back_populates="props")
    name: str = Field(primary_key=True, max_length=32)
    value: str = Field()
