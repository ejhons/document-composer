from dcp_api.api.dependencies import create_container
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dcp_api.api.routes import (
    components,
    projects,
    recipes,
    iteraction,
    compilation
)

def create_app() -> FastAPI:
    container = create_container()

    # Creates app
    app = FastAPI(
        title="Document Composer",
        version="0.1.0",
    )

    # Keeps services and repository information
    app.state.container = container

    # List the origins allowed to make requests
    origins = [
        "http://127.0.0.1:5500"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Use ["*"] to allow all origins (not recommended for production)
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
        allow_headers=["*"],  # Allows all headers
    )

    # Main route
    @app.get('/')
    async def root():
        return {'message':'Doc-Composer'}

    # Add routes
    app.include_router(projects.router)
    app.include_router(components.router)
    app.include_router(recipes.router)
    app.include_router(iteraction.router)
    app.include_router(compilation.router)

    # Add exception handlers
    # app.add_exception_handler(SynapticApiError, api_exception_handler)
    # app.add_exception_handler(SynapticException, core_exception_handler)
    return app


app = create_app()

