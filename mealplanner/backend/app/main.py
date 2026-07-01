"""Smart Meal Planner PL — punkt wejścia aplikacji FastAPI."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1 import router as v1_router
from app.core.config import settings
from app.core.exceptions import AppException
from app.db.session import Base, get_db

logger = logging.getLogger(__name__)


async def _create_tables() -> None:
    """Tworzy tabele w bazie danych (tylko do celów deweloperskich)."""
    from app.db.session import engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Tabele bazy danych zostały utworzone/zweryfikowane.")


async def _seed_database_if_empty() -> None:
    """Wypełnia bazę danych danymi początkowymi, jeśli jest pusta.

    Importuje i uruchamia funkcję seed_database, o ile jest dostępna.
    Błędy seedowania są logowane, ale nie blokują uruchomienia aplikacji.
    """
    try:
        from app.db.seed import seed_database
        from app.db.session import async_session_factory
        from sqlalchemy import select
        from app.models.store import Store

        async with async_session_factory() as db:
            result = await db.execute(select(Store).limit(1))
            if result.first() is None:
                logger.info("Baza danych jest pusta. Rozpoczynam seedowanie...")
                await seed_database(db)
                await db.commit()
                logger.info("Dane początkowe zostały załadowane.")
            else:
                logger.info("Baza danych zawiera już dane. Pomijam seedowanie.")
    except ImportError:
        logger.debug("Moduł seed_database nie jest dostępny — pomijam seedowanie.")
    except Exception:
        logger.exception("Błąd podczas seedowania bazy danych.")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Zarządza cyklem życia aplikacji — startup i shutdown."""
    logger.info("Uruchamianie Smart Meal Planner PL API...")
    await _create_tables()
    await _seed_database_if_empty()
    logger.info("Aplikacja gotowa do obsługi żądań.")
    yield
    logger.info("Zamykanie Smart Meal Planner PL API...")


app = FastAPI(
    title="Smart Meal Planner PL API",
    description="API do planowania posiłków z integracją z polskimi sieciami handlowymi",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://.*\.app\.github\.dev|http://localhost:\d+|http://127\.0\.0\.1:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Exception handlers
# ---------------------------------------------------------------------------


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Obsługuje wyjątki aplikacyjne i zwraca ustandaryzowaną odpowiedź JSON."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.error_code,
        },
    )


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(v1_router, prefix=settings.API_V1_PREFIX)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@app.get(
    "/health",
    tags=["Health"],
    summary="Sprawdzenie stanu aplikacji",
)
async def health_check() -> dict[str, str]:
    """Zwraca status zdrowia aplikacji — używany przez load balancery i monitoring."""
    return {"status": "healthy", "service": "smart-meal-planner-pl"}
