from products_app.models import Product
from products_app.repository import ProductRepository
from products_app.db import get_session


class ProductService:
    @staticmethod
    async def get_product_by_id(product_id: int) -> Product | None:
        async with get_session() as session:
            return await ProductRepository.get_product_by_id(product_id, session)

    @staticmethod
    async def get_active_products() -> list[Product]:
        async with get_session() as session:
            return await ProductRepository.get_active_products(session)

    @staticmethod
    async def search_products_by_name(search: str) -> list[Product]:
        async with get_session() as session:
            return await ProductRepository.search_products_by_name(search, session)

    @staticmethod
    async def create_product(inp: "ProductInput") -> Product:
        async with get_session() as session:
            product = Product(name=inp.name, price=inp.price, status=inp.status)
            return await ProductRepository.create_product(product, session)

    @staticmethod
    async def update_product(product_id: int, inp: "ProductInput") -> Product | None:
        async with get_session() as session:
            product = await ProductRepository.get_product_by_id(product_id, session)
            if product:
                product.name = inp.name
                product.price = inp.price
                product.status = inp.status
                return await ProductRepository.update_product(product, session)
            return None

    @staticmethod
    async def delete_product(product_id: int) -> bool:
        async with get_session() as session:
            product = await ProductRepository.get_product_by_id(product_id, session)
            if product:
                await ProductRepository.delete_product(product, session)
                return True
            return False