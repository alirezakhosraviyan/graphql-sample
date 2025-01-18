from app.db import get_session
from app.products.models import Image, Product


async def create_product(inp: "ProductInput", images: list["ImageInput"] | None) -> Product:  # type: ignore  # noqa
    async with get_session() as session:
        product = Product(
            name=inp.name,
            price=inp.price,
            status=inp.status,
        )
        if images:
            product.images = [Image(url=image.url, priority=image.priority or 100) for image in images]

        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product
