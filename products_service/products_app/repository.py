from sqlmodel import select, func
from sqlmodel.ext.asyncio.session import AsyncSession

from products_app.models import Product, ProductStatus


class ProductRepository:
    @staticmethod
    async def get_product_by_id(product_id: int, session: AsyncSession) -> Product | None:
        stmt = select(Product).where(Product.id == product_id)
        result = await session.scalar(stmt)
        return result

    @staticmethod
    async def get_active_products(session: AsyncSession) -> list[Product]:
        stmt = select(Product).where(Product.status == ProductStatus.ACTIVE)
        result = await session.scalars(stmt)
        return list(result)

    @staticmethod
    async def search_products_by_name(search: str, session: AsyncSession) -> list[Product]:
        stmt = select(Product).where(
            Product.status == ProductStatus.ACTIVE,
            func.to_tsvector("english", Product.name).match(search)
        )
        result = await session.scalars(stmt)
        return list(result.all())

    @staticmethod
    async def create_product(product: Product, session: AsyncSession) -> Product:
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    @staticmethod
    async def update_product(product: Product, session: AsyncSession) -> Product:
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    @staticmethod
    async def delete_product(product: Product, session: AsyncSession) -> None:
        await session.delete(product)
        await session.commit()