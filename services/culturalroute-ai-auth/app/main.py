from fastapi import FastAPI
from app.routers import auth

app = FastAPI(
    title="CulturalRoute AI - Auth Service",
    version="1.0.0",
    description="Servicio de autenticación y gestión de usuarios"
)

app.include_router(auth.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "auth"}

@app.get("/")
async def root():
    return {"message": "Auth Service is running"}