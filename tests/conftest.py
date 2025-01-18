import os
from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from app.db import get_db_engine, get_session
from app.main import app
from app.products.models import Image, Product, ProductStatus


async def seed_data() -> None:
    """Seed the database with initial test data."""
    product1 = Product(name="Product 1", price=10.0, status=ProductStatus.ACTIVE)
    product2 = Product(name="Product 2", price=20.0, status=ProductStatus.INACTIVE)

    async with get_session() as session:
        session.add_all([product1, product2])
        await session.commit()

        image1 = Image(url="http://example.com/image1.jpg", priority=1, product_id=product1.id)
        session.add(image1)

        await session.commit()


@pytest.fixture(scope="function", autouse=True)
async def setup_test_env() -> AsyncGenerator[None, None]:
    """Sets up the database environment for testing."""
    database_uri = os.environ.get("DATABASE_URI", "postgresql+asyncpg://user:password@localhost/test_db")
    engine = get_db_engine(database_uri)
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    await seed_data()
    yield
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def client() -> AsyncGenerator[TestClient, None]:
    """Provide an HTTP client for testing."""
    with TestClient(app) as client:
        yield client
