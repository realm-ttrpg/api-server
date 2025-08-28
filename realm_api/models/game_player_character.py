"""GamePlayer -> Character model"""

# 3rd party
from sqlmodel import Field, SQLModel


class GamePlayerCharacter(SQLModel, table=True):
    __tablename__ = "game_player_character"  # type: ignore

    game_id: int = Field(foreign_key="game.id", primary_key=True)
    character_id: int = Field(foreign_key="character.id", primary_key=True)
    player_id: str = Field(foreign_key="player.user_id", primary_key=True)
