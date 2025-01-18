from app._app import create_app
from app.products.schema import schema as product_schema

app = create_app(schema=product_schema)
