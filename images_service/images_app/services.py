from sqlalchemy.ext.asyncio import AsyncSession

from images_app.db import get_session

from .repository import (
    create_image,
    delete_image,
    get_all_images,
    get_image_by_id,
    get_image_by_product_id,
    update_image,
)


async def create_image_service(session: AsyncSession, url: str, priority: int, product_id: int):
    image_data = {"url": url, "priority": priority, "product_id": product_id}
    return await create_image(session, image_data)


async def get_image_service(session: AsyncSession, image_id: int):
    return await get_image_by_id(session, image_id)


async def get_image_by_product_id_service(product_id: int):
    async with get_session() as session:
        res = await get_image_by_product_id(session, product_id)
        print(res)
        return res


async def get_all_images_service(session: AsyncSession):
    return await get_all_images(session)


async def update_image_service(session: AsyncSession, image_id: int, updates: dict):
    return await update_image(session, image_id, updates)


async def delete_image_service(session: AsyncSession, image_id: int):
    return await delete_image(session, image_id)
