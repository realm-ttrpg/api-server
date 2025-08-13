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


class StartupMiddleware:
    """Startup middleware for initializing the database"""

    initialized: aio.Event = aio.Event()

    def __init__(self, app):
        self.app = app

    @classmethod
    async def init_db(cls):
        """Initializes the database."""

        for mod in [
            "character_prop.CharacterProp",
            "character_stat.CharacterStat",
            "game.Game",
            "guild.Guild",
            "system.System",
            "user_session.UserSession",
        ]:
            import_module(f".models.{mod}", __name__)

        log.info("Initializing database")

        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    async def __call__(self, scope, receive, send):
        if not StartupMiddleware.initialized.is_set():
            await StartupMiddleware.init_db()
            StartupMiddleware.initialized.set()

        await self.app(scope, receive, send)


async def get_session():
    """Get an `AsyncSession` object."""

    async with AsyncSession(async_engine) as session:
        yield session


def setup_webapp(app: FastAPI, *_):
    app.add_middleware(StartupMiddleware)
