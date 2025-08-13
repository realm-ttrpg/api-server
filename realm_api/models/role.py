"""Role model"""

# 3rd party
from sqlmodel import Field, SQLModel


class Role(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str = Field(max_length=32)
