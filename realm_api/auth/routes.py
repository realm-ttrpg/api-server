# stdlib
import json

# 3rd party
from aiohttp import ClientSession
from fastapi import APIRouter, HTTPException, status

# local
from .models import (
    LoginRequest,
    LoginResponse,
    SharedGuildsRequest,
    SharedGuildsResponse,
)
from ..ipc import ipc_op, redis_conn

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(login_request: LoginRequest) -> LoginResponse:
    async with ClientSession() as session:
        session.headers.add("Authorization", f"Bearer {login_request.token}")

        async with session.get(
            "https://discord.com/api/v10/oauth2/@me"
        ) as response:
            obj = await response.json()

            if obj["user"]["id"] != login_request.user_id:
                raise HTTPException(status.HTTP_403_FORBIDDEN)

    # TODO generate, store, and return session token
    return LoginResponse(token="ok")


@router.post("/logout")
def logout():
    # TODO remove session token from DB
    pass


@router.post("/shared-guilds")
async def shared_guilds(
    shared_guilds_request: SharedGuildsRequest,
) -> SharedGuildsResponse:
    CACHE_EXPIRY = 60  # 1 minute

    if cached := redis_conn.get("bot.guilds"):
        bot_guilds = json.loads(cached)  # type: ignore
    else:
        bot_guilds = await ipc_op("guilds", timeout=3)
        redis_conn.setex("bot.guilds", CACHE_EXPIRY, json.dumps(bot_guilds))

    return SharedGuildsResponse(
        guild_ids=set(bot_guilds).intersection(shared_guilds_request.guild_ids),
    )
