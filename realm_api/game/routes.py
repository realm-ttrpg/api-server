"""Game routes"""

# 3rd party
from fastapi import APIRouter, Depends
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

# local
from ..db import get_session
from ..models.game import Game
from .depends import user_in_guild
from .schema import GameResponse

router = APIRouter(prefix="/game")


@router.get("/list/{guild_id}")
async def list_games(
    guild_id: int,
    db: AsyncSession = Depends(get_session),
    in_guild=Depends(user_in_guild),
) -> list[GameResponse]:
    games = (
        await db.exec(select(Game).where(Game.guild_id == str(guild_id)))
    ).all()
    response = [
        GameResponse.model_validate(game, from_attributes=True)
        for game in games
    ]

    return response


@router.get("/{guild_id}/{game_id}")
async def get_game(
    guild_id: int,
    game_id: int,
    db: AsyncSession = Depends(get_session),
    in_guild=Depends(user_in_guild),
) -> GameResponse:
    game = (await db.exec(select(Game).where(Game.id == str(game_id)))).one()
    response = GameResponse.model_validate(game, from_attributes=True)

    return response
