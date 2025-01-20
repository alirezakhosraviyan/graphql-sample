from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from images_app.app import create_app
from images_app.db import get_db_engine, get_session
from images_app.models import Image
from images_app.settings import settings


@pytest.fixture
async def seed_images() -> list[Image]:
    async with get_session() as session:
        images = [
            Image(url="http://example.com/image1.jpg", priority=50, product_id=1),
            Image(url="http://example.com/image2.jpg", priority=20, product_id=2),
            Image(url="http://example.com/image3.jpg", priority=80, product_id=3),
        ]
        session.add_all(images)
        await session.commit()
        return images


@pytest.fixture(scope="function", autouse=True)
async def setup_test_env() -> AsyncGenerator[None, None]:
    """Sets up the database environment for testing."""
    engine = get_db_engine(settings.DATABASE_URI)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def fastapi_client() -> AsyncGenerator[TestClient, None]:
    """Provide an HTTP client for testing."""
    test_app = create_app()
    with TestClient(test_app) as client:
        yield client
