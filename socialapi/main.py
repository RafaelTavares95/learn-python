import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from socialapi.database import database
from socialapi.logging_conf import configure_logging
from socialapi.routers.comment import router as comment_router
from socialapi.routers.post import router as post_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.include_router(post_router)
app.include_router(comment_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the api!"}


@app.get("/ping")
async def ping():
    logger.debug("Ping Request Recieved")
    return "pong!"
