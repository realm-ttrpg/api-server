"""Authentication/authorization routes"""

# 3rd party
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

# suite
from realm_schema import BotGuildsResponse

# local
from realm_api.db import get_session
from realm_api.discord import DiscordClient
from realm_api.models.user_session import UserSession
from realm_api.rpc import redis_conn, rpc_bot
from .depends import require_login
from .schema import LoginRequest, LoginResponse, SharedGuildsResponse

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    login_request: LoginRequest,
    db: AsyncSession = Depends(get_session),
) -> LoginResponse:
    discord = DiscordClient(login_request.user_id, login_request.token)
    obj = await discord.get_user_info()

    if obj["user"]["id"] != login_request.user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN)

    existing = (
        await db.execute(
            select(UserSession).where(
                UserSession.user_id == discord.user_id,
            )
        )
    ).scalar_one_or_none()

    if existing:
        await db.delete(existing)
        await db.commit()

    user_session = UserSession(
        user_id=discord.user_id,
        discord_token=discord.token,
    )
    db.add(user_session)
    await db.commit()
    await db.refresh(user_session)

    return LoginResponse(
        token=user_session.realm_token,
        user=LoginResponse.User(
            id=discord.user_id,
            name=obj["user"]["username"],
            avatar=obj["user"]["avatar"],
        ),
    )


@router.post("/logout")
async def logout(
    db: AsyncSession = Depends(get_session),
    session: UserSession = Depends(require_login),
):
    await db.delete(session)
    await db.flush()


@router.get("/shared-guilds")
async def shared_guilds(
    session: UserSession = Depends(require_login),
) -> SharedGuildsResponse:
    CACHE_EXPIRY = 60  # 1 minute

    discord = DiscordClient(session.user_id, session.discord_token)
    my_guilds = await discord.get_guilds()

    if cached := redis_conn.get("bot.guilds"):
        bot_guilds = (
            BotGuildsResponse.model_validate_json(cached)  # type: ignore
        )
    else:
        bot_guilds = BotGuildsResponse.model_validate_json(
            await rpc_bot("guilds")
        )
        redis_conn.setex(
            "bot.guilds", CACHE_EXPIRY, bot_guilds.model_dump_json()
        )

    return SharedGuildsResponse(
        guilds=[g for g in my_guilds if g["id"] in bot_guilds.guild_ids],
    )
