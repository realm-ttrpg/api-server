"""User session model"""

# stdlib
from uuid import uuid4

# 3rd party
from sqlmodel import Field, SQLModel


class UserSession(SQLModel, table=True):
    user_id: str = Field(primary_key=True, max_length=32)
    discord_token: str = Field(max_length=64)
    realm_token: str = Field(default_factory=uuid4, index=True)
