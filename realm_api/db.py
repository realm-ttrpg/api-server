"""Database functionality and Aethersprite extension"""

# stdlib
import asyncio as aio
from importlib import import_module
import os

# 3rd party
from fastapi import FastAPI
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

# api
from aethersprite import log

DB_URL = os.environ.get(
    "DB_URL", "postgresql+asyncpg://realm:realm@localhost/realm"
)
async_engine = create_async_engine(DB_URL, future=True)


async def get_session():
    """Get an `AsyncSession` object."""

    async with AsyncSession(async_engine) as session:
        yield session


def setup_webapp(app: FastAPI, *_):
    async def init_db():
        for mod in [
            "character",
            "character_prop",
            "character_stat",
            "game",
            "game_player",
            "game_player_role",
            "game_role",
            "guild",
            "player",
            "role",
            "system",
            "user_session",
        ]:
            import_module(f".models.{mod}", __package__)

        log.info("Initializing database")

        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    aio.get_event_loop().run_until_complete(init_db())
