from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.api_router import api_router
from app.db.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize MongoDB connection on startup."""
    await init_db()
    yield


app = FastAPI(
    title="Laptop Service Appointment Service",
    description="Microservice for handling laptop repair and maintenance appointments.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the Laptop Appointment Service"}
