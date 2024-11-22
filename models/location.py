from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel

class Location(BaseModel):
    id: str
    device_id: str
    latitude: float
    longitude: float
    speed: float
    timestamp: datetime
    source: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'Location':
        return Location(
            id=str(data["_id"]),
            device_id=data["device_id"],
            latitude=data["latitude"],
            longitude=data["longitude"],
            speed=data["speed"],
            timestamp=data["timestamp"],
            source=data["source"]
        )
