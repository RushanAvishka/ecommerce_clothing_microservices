from pymongo import AsyncMongoClient
from beanie import init_beanie

from app.core.config import settings
from app.models.appointment import Appointment, AppointmentHistory


async def init_db():
    """Initialize the MongoDB connection and Beanie ODM."""
    client = AsyncMongoClient(settings.MONGODB_URL)
    database = client[settings.DATABASE_NAME]

    await init_beanie(
        database=database,
        document_models=[Appointment, AppointmentHistory],
    )
