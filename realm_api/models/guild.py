"""Discord Guild model"""

# 3rd party
from sqlmodel import Field, SQLModel


class Guild(SQLModel, table=True):
    id: str = Field(primary_key=True, max_length=32)
