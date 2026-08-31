from fastapi import FastAPI

from dcp_api.api.routes import (
    projects,
    files,
    recipes,
)

# app = FastAPI()



def create_app() -> FastAPI:
    # Creates app
    app = FastAPI(
        title="Document Composer",
        version="0.1.0",
    )

    # Main route
    @app.get('/')
    async def root():
        return {'message':'Doc-Composer'}

    # Add routes
    app.include_router(projects.router)
    app.include_router(files.router)
    app.include_router(recipes.router)

    # Add exception handlers
    # app.add_exception_handler(SynapticApiError, api_exception_handler)
    # app.add_exception_handler(SynapticException, core_exception_handler)
    return app


app = create_app()

