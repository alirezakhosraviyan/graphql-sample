from fastapi.testclient import TestClient

from images_app.models import Image


async def test_create_image(fastapi_client: TestClient) -> None:
    query = """
        mutation CreateImage($input: ImageInput!) {
            createImage(inp: $input) {
                url
                priority
                productId
            }
        }
    """
    variables = {"input": {"url": "http://example.com/image4.jpg", "priority": 90, "productId": 4}}
    response = fastapi_client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()

    # Assertions
    assert "errors" not in data
    assert data["data"]["createImage"]["url"] == "http://example.com/image4.jpg"
    assert data["data"]["createImage"]["priority"] == 90
    assert data["data"]["createImage"]["productId"] == 4


async def test_get_all_images(fastapi_client: TestClient, seed_images: list[Image]) -> None:
    query = """
        query {
            getAllImages {
                url
                priority
                productId
            }
        }
    """
    response = fastapi_client.post("/graphql", json={"query": query})
    data = response.json()

    # Assertions
    assert "errors" not in data
    images = data["data"]["getAllImages"]
    assert len(images) == len(seed_images)
    for image, expected in zip(images, seed_images, strict=False):
        assert image["url"] == expected.url
        assert image["priority"] == expected.priority
        assert image["productId"] == expected.product_id


async def test_delete_image(fastapi_client: TestClient, seed_images: list[Image]) -> None:
    query = """
        mutation DeleteImage($imageId: Int!) {
            deleteImage(imageId: $imageId)
        }
    """
    variables = {"imageId": 3}  # Deleting the image with product_id = 3
    response = fastapi_client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()

    # Assertions
    assert "errors" not in data
    assert data["data"]["deleteImage"] == "Image deleted successfully."


async def test_get_image_by_id(fastapi_client: TestClient, seed_images: list[Image]) -> None:
    query = """
        query GetImage($imageId: Int!) {
            getImage(imageId: $imageId) {
                url
                priority
                productId
            }
        }
    """
    variables = {"imageId": 2}  # Get the image with product_id = 2
    response = fastapi_client.post("/graphql", json={"query": query, "variables": variables})
    data = response.json()

    # Assertions
    assert "errors" not in data
    expected_image = seed_images[1]  # Index 1 corresponds to product_id = 2
    assert data["data"]["getImage"]["url"] == expected_image.url
    assert data["data"]["getImage"]["priority"] == expected_image.priority
    assert data["data"]["getImage"]["productId"] == expected_image.product_id
