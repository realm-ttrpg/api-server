# stdlib
import json
from multiprocessing import Queue
from uuid import uuid4

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
from ..ipc import pubsub, redis_conn

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
) -> SharedGuildsResponse | None:
    q = Queue()

    def handler(message: dict):
        data = json.loads(message["data"])
        q.put(
            SharedGuildsResponse(
                guild_ids=set(data["guilds"]).intersection(
                    shared_guilds_request.guild_ids
                ),
            )
        )

    uuid = str(uuid4())
    pubsub.subscribe(**{uuid: handler})
    redis_conn.publish("ipc", json.dumps({"uuid": uuid, "op": "guilds"}))
    response = q.get(timeout=3)
    pubsub.unsubscribe(uuid)

    return response
