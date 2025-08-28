"""Database functionality"""

# stdlib
import os

# 3rd party
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

# local
from realm_api.logging import logger


DB_URL = os.environ.get(
    "DB_URL", "postgresql+asyncpg://realm:realm@localhost/realm"
)
async_engine = create_async_engine(DB_URL, future=True)


async def init_db():
    """Initialize the database. Used in the FastAPI application lifespan."""

    from . import models  # noqa: F401

    logger.info("Initializing database")

    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """Get an `AsyncSession` object."""

    async with AsyncSession(async_engine) as session:
        yield session
