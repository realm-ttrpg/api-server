"""Game Player model"""

# 3rd party
from sqlmodel import Field, SQLModel


class GamePlayer(SQLModel, table=True):
    __tablename__ = "game_player"  # type: ignore

    game_id: int = Field(foreign_key="game.id", primary_key=True)
    player_id: str = Field(foreign_key="player.user_id", primary_key=True)
