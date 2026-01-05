from fastapi import FastAPI

from socialapi.routers.comment import router as comment_router
from socialapi.routers.post import router as post_router

app = FastAPI()
app.include_router(post_router)
app.include_router(comment_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the api!"}


@app.get("/ping")
async def ping():
    return "pong!"
