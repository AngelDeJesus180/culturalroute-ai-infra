from fastapi import FastAPI
from app.routers.geo_router import router as geo_router

app = FastAPI(title="Geo Service")

app.include_router(geo_router)
