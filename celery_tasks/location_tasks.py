from celery import Celery
from db.mongodb import get_db
import os
import asyncio
import json

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://mongodb:27017")
CELERY_MONGODB_BACKEND = f"mongodb://{MONGODB_URL.split('://')[-1]}"

celery_app = Celery('tasks',
                    broker=f'mongodb://{MONGODB_URL.split("://")[-1]}/celerydb',
                    backend=f'mongodb://{MONGODB_URL.split("://")[-1]}/celerydb')

@celery_app.task
def process_location(location_data):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    async def save_location():
        try:
            db = await get_db()
            result = await db.locations.insert_one(location_data)
            return {"status": "success", "location_id": str(result.inserted_id)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    return loop.run_until_complete(save_location())
