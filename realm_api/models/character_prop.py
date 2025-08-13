"""Character model"""

# 3rd party
from sqlmodel import Field, SQLModel

# local
from .character import Character


class CharacterProp(SQLModel, table=True):
    character_id: int = Field(foreign_key=Character.id, primary_key=True)
    name: str = Field(primary_key=True, max_length=32)
    value: str = Field()
