from fastapi import FastAPI
from app.routers import places
from app.infrastructure.rabbitmq import rabbitmq_consumer
from app.infrastructure.database import init_db

app = FastAPI(
    title="CulturalRoute AI - Place Service",
    version="1.0.0",
    description="Servicio de catálogo de lugares culturales"
)

app.include_router(places.router)

@app.on_event("startup")
async def startup_event():
    init_db()
    # Iniciar RabbitMQ consumer (ya se inicia automáticamente al importar)
    print("✅ Place Service iniciado con RabbitMQ Consumer")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "place"}

@app.get("/")
async def root():
    return {"message": "Place Service is running"}