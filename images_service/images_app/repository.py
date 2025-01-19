from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from .models import Image


async def create_image(session: AsyncSession, image_data: dict) -> Image:
    image = Image(**image_data)
    session.add(image)
    await session.commit()
    await session.refresh(image)
    return image


async def get_image_by_id(session: AsyncSession, image_id: int) -> Image | None:
    result = await session.scalar(select(Image).where(Image.id == image_id))
    return result


async def get_image_by_product_id(session: AsyncSession, product_id: int) -> Image | None:
    stmt = select(Image).where(Image.product_id == product_id)
    res = await session.execute(stmt)
    return res.first()


async def get_all_images(session: AsyncSession) -> list[Image]:
    result = await session.scalars(select(Image))
    return list(result.all())


async def update_image(session: AsyncSession, image_id: int, updates: dict) -> Image | None:
    image = await get_image_by_id(session, image_id)
    if image:
        for key, value in updates.items():
            setattr(image, key, value)
        session.add(image)
        await session.commit()
        await session.refresh(image)
    return image


async def delete_image(session: AsyncSession, image_id: int) -> bool:
    image = await get_image_by_id(session, image_id)
    if image:
        await session.delete(image)
        await session.commit()
        return True
    return False
