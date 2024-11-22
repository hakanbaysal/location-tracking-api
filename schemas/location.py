from pydantic import BaseModel
from datetime import datetime

class LocationBase(BaseModel):
    device_id: str = "test_device"
    latitude: float
    longitude: float
    speed: float
    timestamp: datetime

class LocationCreate(LocationBase):
    pass

class LocationResponse(BaseModel):
    message: str
    task_id: str
