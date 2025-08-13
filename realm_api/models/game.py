"""Game model"""

# 3rd party
from sqlmodel import Field, SQLModel


class Game(SQLModel, table=True):
    id: int = Field(primary_key=True)
    system_id: int = Field(foreign_key="system.id")
    guild_id: str = Field(foreign_key="guild.id")
    name: str = Field(max_length=128)
