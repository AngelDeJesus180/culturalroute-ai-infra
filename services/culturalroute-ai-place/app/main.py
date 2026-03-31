from fastapi import FastAPI
from app.routers import places

app = FastAPI(
    title="CulturalRoute AI - Place Service",
    version="1.0.0",
    description="Servicio de catálogo de lugares culturales"
)

app.include_router(places.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "place"}

@app.get("/")
async def root():
    return {"message": "Place Service is running"}