"""Konfiguracja aplikacji Smart Meal Planner PL.

Wszystkie ustawienia ładowane są ze zmiennych środowiskowych
z domyślnymi wartościami dla środowiska deweloperskiego.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Główna klasa konfiguracji aplikacji."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # ── Baza danych ──────────────────────────────────────────────
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/mealplanner"
    )

    # ── Redis / Celery ───────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── JWT / Bezpieczeństwo ─────────────────────────────────────
    SECRET_KEY: str = "CHANGE-ME-to-a-long-random-secret-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── Aplikacja ────────────────────────────────────────────────
    APP_NAME: str = "Smart Meal Planner PL"
    API_V1_PREFIX: str = "/api/v1"


settings = Settings()
