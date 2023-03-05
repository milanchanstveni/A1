from fastapi import (
    FastAPI
)
import uvicorn
from tortoise.contrib.fastapi import register_tortoise

from core.logging import LOG
from api.urls import API
from db.utils import get_db_config


APP = FastAPI(
    title="A1",
    description='A1 interview task.',
    version="1.0",
    docs_url="/",
)

register_tortoise(
    app=APP,
    config=get_db_config(),
    generate_schemas=True,
    add_exception_handlers=True,
)


APP.include_router(
    API,
    prefix="/api",
)


@APP.on_event("startup")
async def startup():
    LOG.info("Server started.")


@APP.on_event("shutdown")
async def shutdown():
    LOG.info("Server stopped.")


if __name__ == "__main__":
    uvicorn.run(
        app="services.server:APP",
        host="0.0.0.0",
        port=5000,
        reload=True
    )
