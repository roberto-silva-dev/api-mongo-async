from app.config import settings
from fastapi import FastAPI
from app.models.order import Order
from app.routes import orders
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    client = AsyncIOMotorClient(settings.mongo_url)
    await init_beanie(
        database=client[settings.mongo_db],
        document_models=[Order] 
    )
    yield
    # shutdown
    client.close()

app = FastAPI(
    lifespan=lifespan,
    title="Orders API",
    description="API to orders management",
    version="1.0.0",
)
app.include_router(orders.router)
