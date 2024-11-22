import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from main import app
from db.mongodb import client

test_client = TestClient(app)

@pytest.fixture
async def setup_database():
    await client.locationdb.locations.delete_many({})
    yield
    await client.locationdb.locations.delete_many({})

@pytest.mark.asyncio
async def test_create_location(setup_database):
    location_data = {
        "device_id": "test_device",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "speed": 50.0,
        "timestamp": datetime.now().isoformat()
    }
    response = test_client.post("/api/v1/location", json=location_data)
    assert response.status_code == 200
    assert "task_id" in response.json()

@pytest.mark.asyncio
async def test_get_latest_location(setup_database):
    location_data = {
        "device_id": "test_device",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "speed": 50.0,
        "timestamp": datetime.now().isoformat()
    }
    test_client.post("/api/v1/location", json=location_data)
    
    response = test_client.get("/api/v1/locations/test_device/latest")
    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == "test_device"
