import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware

from socialapi.core.database import database
from socialapi.core.logging_conf import configure_logging
from socialapi.routers.auth import router as auth_router
from socialapi.routers.comment import router as comment_router
from socialapi.routers.like import router as like_router
from socialapi.routers.post import router as post_router
from socialapi.routers.user import router as user_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router)
app.include_router(comment_router)
app.include_router(user_router)
app.include_router(like_router)
app.include_router(auth_router)


@app.exception_handler(HTTPException)
async def http_exception_handle_logging(request, exc):
    logger.error(f"HTTPException: {exc.status_code} - {exc.detail}")
    return await http_exception_handler(request, exc)


@app.get("/")
async def root():
    return {"message": "Welcome to the api!"}


@app.get("/ping")
async def ping():
    logger.debug("Ping Request Recieved")
    return "pong!"
