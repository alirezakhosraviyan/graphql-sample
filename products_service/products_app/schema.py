import strawberry
from products_app.models import ProductStatus
from products_app.services import ProductService


@strawberry.federation.type(keys=["id"])
class ProductType:
    id: int
    name: str
    price: float
    status: ProductStatus


@strawberry.input
class ProductInput:
    name: str
    price: float
    status: ProductStatus = ProductStatus.ACTIVE


@strawberry.type
class Query:
    @strawberry.field
    async def search_active_products_by_name(self, search: str) -> list[ProductType]:
        products = await ProductService.search_products_by_name(search)
        return [
            ProductType(id=product.id, name=product.name, price=product.price, status=product.status)
            for product in products
        ]

    @strawberry.field
    async def get_active_products_sorted_by_id(self) -> list[ProductType]:
        products = await ProductService.get_active_products()
        return [
            ProductType(id=product.id, name=product.name, price=product.price, status=product.status)
            for product in products
        ]


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_product(self, inp: ProductInput) -> ProductType:
        product = await ProductService.create_product(inp)
        return ProductType(
            id=product.id,
            name=product.name,
            price=product.price,
            status=product.status
        )

    @strawberry.mutation
    async def update_product(self, product_id: int, input: ProductInput) -> ProductType | None:
        product = await ProductService.update_product(product_id, input)
        if product:
            return ProductType(
                id=product.id,
                name=product.name,
                price=product.price,
                status=product.status
            )
        return None

    @strawberry.mutation
    async def delete_product(self, product_id: int) -> str:
        success = await ProductService.delete_product(product_id)
        if success:
            return f"Product {product_id} deleted successfully."
        return f"Product {product_id} not found."


schema = strawberry.federation.Schema(query=Query, mutation=Mutation, enable_federation_2=True)