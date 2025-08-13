"""GamePlayer -> GameRole model"""

# 3rd party
from sqlmodel import Field, SQLModel

# local
from .game_player import GamePlayer
from .game_role import GameRole


class GamePlayerRole(SQLModel, table=True):
    game_id: int = Field(foreign_key=GameRole.game_id, primary_key=True)
    role_id: int = Field(foreign_key=GameRole.role_id, primary_key=True)
    player_id: str = Field(foreign_key=GamePlayer.player_id, primary_key=True)
