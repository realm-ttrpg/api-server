"""Game Role model"""

# 3rd party
from sqlmodel import Field, SQLModel


class GameRole(SQLModel, table=True):
    __tablename__ = "game_role"  # type: ignore

    game_id: int = Field(foreign_key="game.id", primary_key=True)
    role_id: int = Field(foreign_key="role.id", primary_key=True)
