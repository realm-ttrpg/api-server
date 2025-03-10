# stdlib
import json

# 3rd party
from aiohttp import ClientSession
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

# local
from ..db import get_session
from ..models.user_session import UserSession
from ..rpc import redis_conn, rpc_bot
from .depends import require_login
from .schema import (
    LoginRequest,
    LoginResponse,
    SharedGuildsRequest,
    SharedGuildsResponse,
)

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    login_request: LoginRequest,
    db: AsyncSession = Depends(get_session),
) -> LoginResponse:
    async with ClientSession() as http:
        http.headers.add("Authorization", f"Bearer {login_request.token}")

        async with http.get(
            "https://discord.com/api/v10/oauth2/@me"
        ) as response:
            obj = await response.json()

            if obj["user"]["id"] != login_request.user_id:
                raise HTTPException(status.HTTP_403_FORBIDDEN)

    existing = (
        await db.execute(
            select(UserSession).where(
                UserSession.user_id == login_request.user_id,
            )
        )
    ).scalar_one_or_none()

    if existing:
        await db.delete(existing)
        await db.commit()

    user_session = UserSession(
        user_id=login_request.user_id,
        discord_token=login_request.token,
    )
    db.add(user_session)
    await db.commit()
    await db.refresh(user_session)

    return LoginResponse(token=user_session.realm_token)


@router.post("/logout")
async def logout(
    db: AsyncSession = Depends(get_session),
    session: UserSession = Depends(require_login),
):
    await db.delete(session)
    await db.flush()


@router.post("/shared-guilds")
async def shared_guilds(
    shared_guilds_request: SharedGuildsRequest,
    _session=Depends(require_login),
) -> SharedGuildsResponse:
    CACHE_EXPIRY = 60  # 1 minute

    if cached := redis_conn.get("bot.guilds"):
        bot_guilds = json.loads(cached)  # type: ignore
    else:
        bot_guilds = await rpc_bot("guilds")
        redis_conn.setex("bot.guilds", CACHE_EXPIRY, json.dumps(bot_guilds))

    return SharedGuildsResponse(
        guild_ids=set(bot_guilds).intersection(shared_guilds_request.guild_ids),
    )
