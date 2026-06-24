"""Database engine and session management for QuantX AI."""

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from quantx.config import get_settings

settings = get_settings()


class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy models."""


engine: AsyncEngine | None = None
async_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Return the async database engine."""
    global engine
    if engine is None:
        engine = create_async_engine(
            str(settings.database.url),
            echo=settings.database.echo,
            pool_size=settings.database.pool_size,
            max_overflow=settings.database.max_overflow,
            pool_pre_ping=True,
            pool_recycle=3600,
        )
    return engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Return the async session factory."""
    global async_session_factory
    if async_session_factory is None:
        async_session_factory = async_sessionmaker(
            get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False,
        )
    return async_session_factory


async def get_session() -> AsyncSession:
    """FastAPI dependency that provides a database session."""
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


async def close_db() -> None:
    """Dispose of the database engine."""
    global engine
    if engine is not None:
        await engine.dispose()
        engine = None


async def health_check() -> bool:
    """Check database connectivity."""
    try:
        async with get_engine().connect() as conn:
            await conn.execute("SELECT 1")
        return True
    except Exception:
        return False
