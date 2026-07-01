"""Konfiguracja asynchronicznej sesji SQLAlchemy."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_size=10,
    max_overflow=20,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Bazowa klasa deklaratywna dla wszystkich modeli ORM."""

    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dostawca sesji bazodanowej do wstrzykiwania zależności (Depends).

    Yields:
        Asynchroniczna sesja SQLAlchemy.
    """
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
