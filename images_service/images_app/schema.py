import strawberry

from .db import get_session
from .services import (
    create_image_service,
    delete_image_service,
    get_all_images_service,
    get_image_service,
    get_images_by_product_id_service,
    update_image_service,
)


@strawberry.federation.type(keys=["id"])
class ImageType:
    id: int
    url: str
    priority: int
    product_id: int


@strawberry.input
class ImageInput:
    url: str
    priority: int = 100
    product_id: int


@strawberry.federation.type(keys=["id"])
class ProductType:
    id: int

    @strawberry.field
    async def images(self) -> list[ImageType]:
        images = await get_images_by_product_id_service(self.id)
        return [ImageType(**image.model_dump()) for image in images]


@strawberry.type
class Query:
    @strawberry.field
    async def get_image(self, image_id: int) -> ImageType | None:
        async with get_session() as session:
            image = await get_image_service(session, image_id)
            return ImageType(**image.model_dump()) if image else None

    @strawberry.field
    async def get_all_images(self) -> list[ImageType]:
        async with get_session() as session:
            images = await get_all_images_service(session)
            return [ImageType(**image.model_dump()) for image in images]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_image(self, inp: ImageInput) -> ImageType:
        async with get_session() as session:
            image = await create_image_service(session, inp.url, inp.priority, inp.product_id)
            return ImageType(**image.model_dump())

    @strawberry.mutation
    async def update_image(self, image_id: int, updates: ImageInput) -> ImageType | None:
        async with get_session() as session:
            image = await update_image_service(session, image_id, strawberry.asdict(updates))
            return ImageType(**image.model_dump()) if image else None

    @strawberry.mutation
    async def delete_image(self, image_id: int) -> str:
        async with get_session() as session:
            success = await delete_image_service(session, image_id)
            return "Image deleted successfully." if success else "Image not found."


schema = strawberry.federation.Schema(
    query=Query, types=[ImageType, ProductType], mutation=Mutation, enable_federation_2=True
)
