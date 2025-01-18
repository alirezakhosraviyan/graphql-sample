from fastapi import FastAPI
from strawberry import Schema
from strawberry.asgi import GraphQL


def create_app(schema: Schema) -> FastAPI:
    app = FastAPI(title="GraphQL sample")

    # register all features of application
    app.add_route("/graphql", GraphQL(schema=schema, debug=True))  # type: ignore
    return app
