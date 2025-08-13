"""Character stat model"""

# 3rd party
from sqlmodel import Field, SQLModel


class CharacterStat(SQLModel, table=True):
    __tablename__ = "character_stat"  # type: ignore

    character_id: int = Field(foreign_key="character.id", primary_key=True)
    name: str = Field(primary_key=True, max_length=32)
    value: int = Field()
