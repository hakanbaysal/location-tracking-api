from motor.motor_asyncio import AsyncIOMotorClient
from config.settings import settings

client = AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DATABASE_NAME]

async def init_indexes():
    """Initialize MongoDB indexes"""
    await db.locations.create_index([("device_id", 1)])
    await db.locations.create_index([("timestamp", -1)])
    await db.locations.create_index([
        ("device_id", 1),
        ("timestamp", -1)
    ])

async def get_db():
    return db
