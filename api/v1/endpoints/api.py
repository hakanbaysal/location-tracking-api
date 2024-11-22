from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import List
from models.location import Location
from schemas.location import LocationCreate, LocationResponse
from db.mongodb import get_db
from celery_tasks.location_tasks import process_location

router = APIRouter()

@router.post("/location", response_model=LocationResponse)
async def create_location(location: LocationCreate):
    loc_dict = location.dict()
    loc_dict["source"] = "api"
    task = process_location.delay(loc_dict)
    return {"message": "Location data queued for processing", "task_id": task.id}

@router.get("/locations/{device_id}/latest", response_model=Location)
async def get_latest_location(device_id: str):
    db = await get_db()
    location = await db.locations.find_one(
        {"device_id": device_id},
        sort=[("timestamp", -1)]
    )
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return Location.from_dict(location)

@router.get("/locations/{device_id}/range", response_model=List[Location])
async def get_locations_by_date_range(
    device_id: str,
    start_date: datetime,
    end_date: datetime
):
    db = await get_db()
    locations = await db.locations.find({
        "device_id": device_id,
        "timestamp": {
            "$gte": start_date,
            "$lte": end_date
        }
    }).to_list(None)
    return [Location.from_dict(loc) for loc in locations]
