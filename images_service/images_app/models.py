import sqlalchemy as sa
from sqlmodel import Field, SQLModel


class Image(SQLModel, table=True):
    id: int = Field(primary_key=True)
    url: str = Field(nullable=False)
    priority: int = Field(
        default=100,
        sa_column=sa.Column(sa.Integer, sa.CheckConstraint("priority >= 0 AND priority <= 100"), nullable=False),
    )
    product_id: int = Field(nullable=False)

    __table_args__ = (
        sa.Index("idx_priority", "priority"),
        sa.UniqueConstraint("product_id", "url", name="unique_product_id_url"),
    )
