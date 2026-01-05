from contextlib import asynccontextmanager

from fastapi import FastAPI

from socialapi.database import database
from socialapi.routers.comment import router as comment_router
from socialapi.routers.post import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
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
    return "pong!"
