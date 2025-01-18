from enum import Enum

import sqlalchemy as sa
from sqlmodel import Field, Relationship, SQLModel


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

    images: list["Image"] = Relationship(back_populates="product", sa_relationship_kwargs={"lazy": "selectin"})

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


class Image(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    url: str = Field(nullable=False)
    priority: int = Field(default=100, nullable=False)
    product_id: int = Field(foreign_key="product.id", nullable=False)

    product: Product = Relationship(back_populates="images")

    __table_args__ = (sa.Index("idx_priority", "priority"),)
