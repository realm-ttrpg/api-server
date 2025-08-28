"""User session model"""

# stdlib
from uuid import uuid4

# 3rd party
from sqlmodel import Field, SQLModel


def uuid_factory():
    return str(uuid4())


class UserSession(SQLModel, table=True):
    __tablename__ = "user_session"  # type: ignore

    user_id: str = Field(primary_key=True, max_length=32)
    discord_token: str = Field(max_length=64)
    realm_token: str = Field(
        default_factory=uuid_factory, index=True, max_length=36
    )
