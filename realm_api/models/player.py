"""Player model"""

# 3rd party
from sqlmodel import Field, SQLModel


class Player(SQLModel, table=True):
    user_id: str = Field(primary_key=True, max_length=32)
    name: str = Field(max_length=32)
