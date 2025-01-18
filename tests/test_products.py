from fastapi.testclient import TestClient


async def test_search_active_products_by_name(client: TestClient) -> None:
    query = """
    query {
        searchActiveProductsByName(search: "Product") {
            id
            name
            price
            status
            images {
                id
                url
                priority
            }
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()["data"]["searchActiveProductsByName"]
    assert len(data) > 0
    assert data[0]["name"].startswith("Product")


async def test_get_active_products_sorted_by_id(client: TestClient) -> None:
    query = """
    query {
        getActiveProductsSortedById {
            id
            name
            price
            status
            images {
                id
                url
                priority
            }
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()["data"]["getActiveProductsSortedById"]
    assert len(data) > 0
    assert data[0]["status"] == "active"


async def test_get_active_products_sorted_by_price(client: TestClient) -> None:
    query = """
    query {
        getActiveProductsSortedByPrice(order: "asc") {
            id
            name
            price
            status
            images {
                id
                url
                priority
            }
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    data = response.json()["data"]["getActiveProductsSortedByPrice"]
    assert len(data) > 0
    assert data[0]["price"] <= data[-1]["price"]


async def test_create_product(client: TestClient) -> None:
    mutation = """
    mutation {createProduct(inp: {name: "New Product", price: 50.0, status: ACTIVE},
        images: [{url: "http://example.com/image.jpg", priority: 1}]) {
            id
            name
            price
            status
            images {
                id
                url
                priority
            }
        }
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    data = response.json()["data"]["createProduct"]
    assert data["name"] == "New Product"
    assert len(data["images"]) == 1
    assert data["images"][0]["url"] == "http://example.com/image.jpg"


async def test_add_image_to_product(client: TestClient) -> None:
    mutation = """
    mutation {
        addImageToProduct(productId: 1, imageInput: {url: "http://example.com/new_image.jpg", priority: 2}) {
            id
            name
            price
            status
            images {
                id
                url
                priority
            }
        }
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    data = response.json()["data"]["addImageToProduct"]
    assert len(data["images"]) > 1
    assert any(image["url"] == "http://example.com/new_image.jpg" for image in data["images"])


async def test_delete_image(client: TestClient) -> None:
    mutation = """
    mutation {
        deleteImage(imageId: 1)
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    data = response.json()["data"]["deleteImage"]
    assert "Image with id 1 has been deleted" in data


async def test_update_product(client: TestClient) -> None:
    mutation = """
    mutation {
        updateProduct(productId: 1, input: {name: "Updated Product", price: 100.0, status: INACTIVE}) {
            id
            name
            price
            status
            images {
                id
                url
                priority
            }
        }
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    assert response.status_code == 200
    data = response.json()["data"]["updateProduct"]
    assert data["name"] == "Updated Product"
    assert data["status"] == "inactive"
