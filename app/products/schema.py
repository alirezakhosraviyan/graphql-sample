import strawberry
from sqlmodel import func, select
from strawberry import Schema

from app.db import get_session
from app.products.models import Image, Product, ProductStatus
from app.products.repository import create_product


@strawberry.type
class ImageType:
    id: int
    url: str
    priority: int


@strawberry.type
class ProductType:
    id: int
    name: str
    price: float
    status: str
    images: list[ImageType]


@strawberry.input
class ProductInput:
    name: str
    price: float
    status: ProductStatus = ProductStatus.ACTIVE


@strawberry.input
class ImageInput:
    url: str
    priority: int | None = 100


@strawberry.type
class Query:
    @strawberry.field
    async def search_active_products_by_name(self, search: str) -> list[ProductType]:
        async with get_session() as session:
            stmt = select(Product).where(
                Product.status == ProductStatus.ACTIVE,
                func.to_tsvector("english", Product.name).match(search),
            )
            results = await session.execute(stmt)
            products = results.scalars().all()

            return [
                ProductType(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    status=product.status,
                    images=[ImageType(id=image.id, url=image.url, priority=image.priority) for image in product.images],
                )
                for product in products
                if product.id
            ]

    @strawberry.field
    async def get_active_products_sorted_by_id(self) -> list[ProductType]:
        async with get_session() as session:
            stmt = select(Product).where(Product.status == ProductStatus.ACTIVE).order_by(Product.id.asc())  # type: ignore
            results = await session.execute(stmt)
            products = results.scalars().all()

            return [
                ProductType(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    status=product.status,
                    images=[ImageType(id=image.id, url=image.url, priority=image.priority) for image in product.images],
                )
                for product in products
                if product.id
            ]

    @strawberry.field
    async def get_active_products_sorted_by_price(self, order: str = "asc") -> list[ProductType]:
        async with get_session() as session:
            sort_order = Product.price.asc() if order == "asc" else Product.price.desc()  # type: ignore
            stmt = select(Product).where(Product.status == ProductStatus.ACTIVE).order_by(sort_order)
            results = await session.execute(stmt)
            products = results.scalars().all()

            return [
                ProductType(
                    id=product.id,
                    name=product.name,
                    price=product.price,
                    status=product.status,
                    images=[ImageType(id=image.id, url=image.url, priority=image.priority) for image in product.images],
                )
                for product in products
                if product.id
            ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_product(self, inp: ProductInput, images: list[ImageInput] | None = None) -> ProductType:
        product = await create_product(inp, images)
        return ProductType(
            id=product.id,
            name=product.name,
            price=product.price,
            status=product.status,
            images=[
                ImageType(id=image.id, url=image.url, priority=image.priority) for image in product.images if image.id
            ],
        )

    @strawberry.mutation
    async def add_image_to_product(self, product_id: int, image_input: ImageInput) -> ProductType:
        async with get_session() as session:
            stmt = select(Product).where(Product.id == product_id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()

            if not product:
                raise Exception(f"Product with id {product_id} not found.")

            new_image = Image(url=image_input.url, priority=image_input.priority or 100)
            product.images.append(new_image)

            session.add(product)
            await session.commit()
            await session.refresh(product)

            return ProductType(
                id=product.id,
                name=product.name,
                price=product.price,
                status=product.status,
                images=[
                    ImageType(id=image.id, url=image.url, priority=image.priority)
                    for image in product.images
                    if image.id
                ],
            )

    @strawberry.mutation
    async def delete_image(self, image_id: int) -> str:
        async with get_session() as session:
            stmt = select(Image).where(Image.id == image_id)
            result = await session.execute(stmt)
            image = result.scalar_one_or_none()

            if not image:
                raise Exception(f"Image with id {image_id} not found.")

            await session.delete(image)
            await session.commit()
            return f"Image with id {image_id} has been deleted."

    @strawberry.mutation
    async def update_product(self, product_id: int, input: ProductInput) -> ProductType:
        async with get_session() as session:
            stmt = select(Product).where(Product.id == product_id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()

            if not product:
                raise Exception(f"Product with id {product_id} not found.")

            product.name = input.name
            product.price = input.price
            product.status = input.status

            session.add(product)
            await session.commit()
            await session.refresh(product)

            return ProductType(
                id=product.id,
                name=product.name,
                price=product.price,
                status=product.status,
                images=[ImageType(id=image.id, url=image.url, priority=image.priority) for image in product.images],
            )

    @strawberry.mutation
    async def delete_product(self, product_id: int) -> str:
        async with get_session() as session:
            stmt = select(Product).where(Product.id == product_id)
            result = await session.execute(stmt)
            product = result.scalar_one_or_none()

            if not product:
                raise Exception(f"Product with id {product_id} not found.")

            await session.delete(product)
            await session.commit()
            return f"Product with id {product_id} has been deleted."


schema = Schema(query=Query, mutation=Mutation)
