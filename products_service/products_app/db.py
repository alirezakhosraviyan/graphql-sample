from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from products_app.settings import settings


def get_db_engine(database_url: str) -> AsyncEngine:
    """
    Creates async engine for a given database url
    """
    return create_async_engine(
        database_url,
        echo=False,
        future=True,
    )


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    """
    Creates async session for a given engine
    """
    engine = get_db_engine(settings.DATABASE_URI)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
