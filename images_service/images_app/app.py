from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

from .schema import schema


def create_app() -> FastAPI:
    app = FastAPI(title="Images Service")
    graphql_app = GraphQLRouter(schema)
    app.include_router(graphql_app, prefix="/graphql")
    return app
