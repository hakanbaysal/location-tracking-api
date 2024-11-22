from fastapi import FastAPI
from api.v1.endpoints import router as api_router
from config.settings import settings
from db.mongodb import init_indexes

app = FastAPI(title="Location Tracking API")
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

@app.on_event("startup")
async def startup_event():
    await init_indexes()
