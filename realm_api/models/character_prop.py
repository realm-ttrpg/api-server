"""Character property model"""

# 3rd party
from sqlmodel import Field, SQLModel


class CharacterProp(SQLModel, table=True):
    __tablename__ = "character_prop"  # type: ignore

    character_id: int = Field(foreign_key="character.id", primary_key=True)
    name: str = Field(primary_key=True, max_length=32)
    value: str = Field()
