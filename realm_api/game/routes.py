"""Game routes"""

# 3rd party
from fastapi import APIRouter, Depends

# local
from ..auth.depends import require_login
from ..models.user_session import UserSession
from .schema import GameResponse

router = APIRouter(prefix="/game")


@router.get("/list/{guild_id}")
def list_games(
    guild_id: int, session: UserSession = Depends(require_login)
) -> list[GameResponse]:
    return [
        GameResponse(id=1234, name="Butts"),
        GameResponse(id=2345, name="Moar butts"),
    ]


@router.get("/{game_id}")
def get_game(
    game_id: int,
    session: UserSession = Depends(require_login),
) -> GameResponse:
    return GameResponse(id=1234, name="Butts")
