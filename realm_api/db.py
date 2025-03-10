# stdlib
import asyncio as aio
import os

# 3rd party
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

DB_URL = os.environ.get(
    "DB_URL", "postgresql+asyncpg://realm:realm@localhost/realm"
)
async_engine = create_async_engine(DB_URL)


async def get_session():
    async with AsyncSession(async_engine) as session:
        yield session


def setup_webapp(*_):
    from .models.user_session import UserSession  # noqa: F401

    async def init_db():
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

    aio.new_event_loop().run_until_complete(init_db())
