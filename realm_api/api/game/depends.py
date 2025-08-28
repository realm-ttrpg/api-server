"""FastAPI checks for use in `Depends()`"""

# 3rd party
from fastapi import Depends, HTTPException, Path, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# local
from realm_api.api.auth.depends import require_login
from realm_api.db import get_session
from realm_api.models.game import Game
from realm_api.models.game_player import GamePlayer
from realm_api.models.user_session import UserSession


async def user_in_guild(
    guild_id: int = Path(),
    session: UserSession = Depends(require_login),
    db: AsyncSession = Depends(get_session),
):
    if not (
        await db.exec(
            select(1)
            .select_from(GamePlayer, Game)
            .where(
                Game.guild_id == str(guild_id),
                GamePlayer.game_id == Game.id,
                GamePlayer.player_id == session.user_id,
            )
        )
    ).one_or_none():
        raise HTTPException(status.HTTP_403_FORBIDDEN)
