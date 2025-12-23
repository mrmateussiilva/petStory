"""Database configuration and session management."""

import logging
from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create engine
# For SQLite, we need check_same_thread=False for FastAPI
connect_args = {"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
)


def init_db() -> None:
    """Initialize database by creating all tables."""
    logger.info(f"Initializing database: {settings.DATABASE_URL}")
    # Import models to register them with SQLModel metadata
    from app.models import Payment  # noqa: F401
    SQLModel.metadata.create_all(engine)
    logger.info("Database tables created successfully")


def get_session() -> Generator[Session, None, None]:
    """Dependency for getting database session (for FastAPI dependencies)."""
    with Session(engine) as session:
        yield session

