from enum import Enum

import sqlalchemy as sa
from sqlmodel import Field, SQLModel


class ProductStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Product(SQLModel, table=True):
    """
    Product Model representing product table

    Indices:
     -  Full-text search index on `name`
     -  Index for queries on `status` sorted by `id`.
     -  Index for active products sorted by `price`.
    """

    id: int = Field(primary_key=True)
    name: str = Field(min_length=3, max_length=500, nullable=False, unique=True)
    price: float = Field(default=0.0, nullable=False)
    status: ProductStatus = Field(default=ProductStatus.ACTIVE, nullable=False)

    __table_args__ = (
        sa.Index(
            "idx_name_fulltext",
            sa.text("to_tsvector('english', name)"),
            postgresql_using="gin",
        ),
        # Index for queries on status and id
        sa.Index("idx_status_id", "status", "id"),
        # Index for active products sorted by price
        sa.Index("idx_status_price", "status", "price"),
    )
