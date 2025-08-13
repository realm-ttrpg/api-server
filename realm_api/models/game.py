"""Game model"""

# 3rd party
from sqlmodel import Field, SQLModel

# local
from .guild import Guild
from .system import System


class Game(SQLModel, table=True):
    id: int = Field(primary_key=True)
    system_id: int = Field(foreign_key=System.id)
    guild_id: str = Field(foreign_key=Guild.id)
    name: str = Field(max_length=128)
