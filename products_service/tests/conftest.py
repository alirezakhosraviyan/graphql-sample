import os
from collections.abc import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from products_app.db import get_db_engine, get_session
from products_app.app import create_app
from products_app.models import Product, ProductStatus


async def seed_data() -> None:
    """Seed the database with initial test data."""
    product1 = Product(name="Product 1", price=10.0, status=ProductStatus.ACTIVE)
    product2 = Product(name="Product 2", price=20.0, status=ProductStatus.INACTIVE)

    async with get_session() as session:
        session.add_all([product1, product2])
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
    app = create_app()
    with TestClient(app) as client:
        yield client
