# stdlib
import json

# 3rd party
from aiohttp import ClientSession
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select, Session

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
    session: Session = Depends(get_session),
) -> LoginResponse:
    async with ClientSession() as http:
        http.headers.add("Authorization", f"Bearer {login_request.token}")

        async with http.get(
            "https://discord.com/api/v10/oauth2/@me"
        ) as response:
            obj = await response.json()

            if obj["user"]["id"] != login_request.user_id:
                raise HTTPException(status.HTTP_403_FORBIDDEN)

    existing = session.exec(
        select(UserSession).where(
            UserSession.user_id == login_request.user_id,
        )
    ).one_or_none()

    if existing:
        session.delete(existing)
        session.commit()

    user_session = UserSession(
        user_id=login_request.user_id,
        discord_token=login_request.token,
    )
    session.add(user_session)
    session.commit()

    return LoginResponse(token=user_session.realm_token)


@router.post("/logout")
def logout(
    session: Session = Depends(get_session),
    user_session: UserSession = Depends(require_login),
):
    session.delete(user_session)
    session.flush()


@router.post("/shared-guilds")
async def shared_guilds(
    shared_guilds_request: SharedGuildsRequest,
    user_session: UserSession = Depends(require_login),
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
