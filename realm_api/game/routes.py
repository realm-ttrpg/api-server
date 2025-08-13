"""Game routes"""

# 3rd party
from fastapi import APIRouter, Depends

# local
from ..auth.depends import require_login
from ..models.user_session import UserSession

router = APIRouter(prefix="/game")


@router.get("/{guild_id}")
def list_games(guild_id: int, session: UserSession = Depends(require_login)):
    return {"games": ["butts"]}
