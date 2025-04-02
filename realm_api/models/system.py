"""Game System model"""

# 3rd party
from sqlmodel import Field, SQLModel


class System(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=128)
    slug: str = Field(max_length=16, unique=True)
