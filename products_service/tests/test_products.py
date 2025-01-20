from fastapi.testclient import TestClient


async def test_search_active_products_by_name(client: TestClient) -> None:
    """Test searching for active products by name."""
    query = """
    query SearchActiveProducts($search: String!) {
      searchActiveProductsByName(search: $search) {
        id
        name
        price
        status
      }
    }
    """
    variables = {"search": "Product 1"}
    response = client.post(
        "/graphql",
        json={"query": query, "variables": variables},
    )

    assert response.status_code == 200

    data = response.json()["data"]["searchActiveProductsByName"]
    assert len(data) == 1
    assert data[0]["name"] == "Product 1"
    assert data[0]["status"] == "ACTIVE"


async def test_get_active_products_sorted_by_id(client: TestClient) -> None:
    """Test retrieving all active products sorted by ID."""
    query = """
    query GetActiveProducts {
      getActiveProductsSortedById {
        id
        name
        price
        status
      }
    }
    """
    response = client.post("/graphql", json={"query": query})
    assert response.status_code == 200

    data = response.json()["data"]["getActiveProductsSortedById"]
    assert len(data) == 1  # Only one active product in the seed data
    assert data[0]["name"] == "Product 1"
    assert data[0]["status"] == "ACTIVE"


async def test_create_product(client: TestClient) -> None:
    """Test creating a new product."""
    mutation = """
    mutation CreateProduct($input: ProductInput!) {
      createProduct(inp: $input) {
        id
        name
        price
        status
      }
    }
    """
    variables = {"input": {"name": "Product 3", "price": 30.0, "status": "ACTIVE"}}
    response = client.post(
        "/graphql",
        json={"query": mutation, "variables": variables},
    )

    assert response.status_code == 200

    data = response.json()["data"]["createProduct"]
    assert data["name"] == "Product 3"
    assert data["price"] == 30.0
    assert data["status"] == "ACTIVE"


async def test_update_product(client: TestClient) -> None:
    """Test updating an existing product."""
    mutation = """
    mutation UpdateProduct($productId: Int!, $input: ProductInput!) {
      updateProduct(productId: $productId, input: $input) {
        id
        name
        price
        status
      }
    }
    """
    variables = {
        "productId": 1,
        "input": {"name": "Updated Product 1", "price": 15.0, "status": "ACTIVE"},
    }
    response = client.post(
        "/graphql",
        json={"query": mutation, "variables": variables},
    )

    assert response.status_code == 200

    data = response.json()["data"]["updateProduct"]
    assert data["name"] == "Updated Product 1"
    assert data["price"] == 15.0
    assert data["status"] == "ACTIVE"


async def test_delete_product(client: TestClient) -> None:
    """Test deleting a product."""
    mutation = """
    mutation DeleteProduct($productId: Int!) {
      deleteProduct(productId: $productId)
    }
    """
    variables = {"productId": 1}
    response = client.post(
        "/graphql",
        json={"query": mutation, "variables": variables},
    )

    assert response.status_code == 200
    data = response.json()["data"]["deleteProduct"]
    assert data == "Product 1 deleted successfully."
