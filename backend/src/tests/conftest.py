import tempfile
import os
os.environ["TESTING"] = "true"

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel

from src.core import database
from main import app


TEST_SECRET_KEY = "testsecret"
TEST_ALGORITHM = "HS256"
TEST_TOKEN_EXPIRE_MINUTES = 30


@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    monkeypatch.setattr("src.core.token.SECRET_KEY", TEST_SECRET_KEY)
    monkeypatch.setattr("src.core.token.ALGORITHM", TEST_ALGORITHM)
    monkeypatch.setattr(
        "src.core.token.ACCESS_TOKEN_EXPIRE_MINUTES", TEST_TOKEN_EXPIRE_MINUTES)


@pytest.fixture(autouse=True)
def mock_rate_limiter(monkeypatch):
    """Disable rate limiting during tests"""
    from unittest.mock import AsyncMock

    # Mock init to do nothing
    async def mock_init(*args, **kwargs):
        pass

    # Mock close to do nothing
    async def mock_close(*args, **kwargs):
        pass

    try:
        from fastapi_limiter import FastAPILimiter

        # Mock the init method
        monkeypatch.setattr(FastAPILimiter, "init", mock_init)
        monkeypatch.setattr(FastAPILimiter, "close", mock_close)

        # Mock the redis attribute
        mock_redis = AsyncMock()
        mock_redis.close = AsyncMock()
        mock_redis.aclose = AsyncMock()
        monkeypatch.setattr(FastAPILimiter, "redis", mock_redis)

    except ImportError:
        pass  # fastapi_limiter not installed


@pytest.fixture
def sample_user():
    from src.models.user import User  # Import here instead
    return User(
        id=1,
        email="test@example.com",
        username="IslamAhmd",
        name="Islam Ahmed",
        password="password123"
    )


@pytest.fixture(scope="function")
def test_db():
    # Import models here to avoid circular import
    from src.models.user import User
    from src.models.chat_history import ChatHistory

    # Create temporary database file
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    test_db_url = f"sqlite:///{db_path}"

    test_engine = create_engine(
        test_db_url,
        connect_args={"check_same_thread": False},
        echo=False
    )

    SQLModel.metadata.create_all(test_engine)

    # Replace the global engine in database module
    original_engine = database.engine
    database.engine = test_engine

    # Create test db
    with Session(test_engine) as test_db:
        yield test_db

    # Restore original engine
    database.engine = original_engine

    # Cleanup
    test_engine.dispose()
    os.close(db_fd)
    os.unlink(db_path)


# TestClient for integration tests
@pytest.fixture
def client(test_db):
    with TestClient(app) as test_client:
        yield test_client
