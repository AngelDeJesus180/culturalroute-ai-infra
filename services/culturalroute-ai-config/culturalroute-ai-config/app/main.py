# ============================================================
# MAIN - Punto de entrada del Config Service
# Aquí se crea la aplicación FastAPI, se registran las rutas
# y se inicializa la base de datos al arrancar.
# ============================================================

from fastapi import FastAPI
from app.routers import config
from app.infrastructure.database import create_tables, engine, SessionLocal
from app.infrastructure.repositories import SQLConfigRepository
from app.application.config_service import ConfigService
from datetime import datetime, timezone

app = FastAPI(
    title="CulturalRoute AI – Config Service",
    description=(
        "Microservicio responsable de centralizar los parámetros configurables del sistema. "
        "Permite consultar y actualizar valores como pesos del scoring, radios de cercanía "
        "y límites operativos sin modificar el código fuente."
    ),
    version="1.0.0"
)

# Registrar las rutas del módulo config
app.include_router(config.router)


@app.on_event("startup")
def on_startup():
    """
    Se ejecuta automáticamente cuando el servicio arranca.
    Crea las tablas en la BD y carga parámetros iniciales si la tabla está vacía.
    """
    create_tables()
    _seed_default_params()


def _seed_default_params():
    """
    Inserta parámetros por defecto si la base de datos está vacía.
    Esto garantiza que el sistema siempre tenga valores de referencia.
    """
    db = SessionLocal()
    try:
        repo = SQLConfigRepository(db)
        service = ConfigService(repo)

        defaults = [
            {
                "key": "scoring_weight_quality",
                "value": "0.3",
                "description": "Peso del criterio 'calidad de datos' en el cálculo del score"
            },
            {
                "key": "scoring_weight_cultural_relevance",
                "value": "0.4",
                "description": "Peso del criterio 'relevancia cultural' en el cálculo del score"
            },
            {
                "key": "scoring_weight_accessibility",
                "value": "0.3",
                "description": "Peso del criterio 'accesibilidad' en el cálculo del score"
            },
            {
                "key": "geo_nearby_radius_km",
                "value": "5.0",
                "description": "Radio en kilómetros para búsqueda de lugares cercanos"
            },
            {
                "key": "route_max_places",
                "value": "5",
                "description": "Número máximo de lugares que puede incluir una ruta sugerida"
            },
        ]

        existing = repo.get_all()
        existing_keys = {p.config_key for p in existing}

        for d in defaults:
            if d["key"] not in existing_keys:
                service.create_parameter(d["key"], d["value"], d["description"])
    finally:
        db.close()


@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint de salud requerido por el proyecto.
    Docker y otros servicios lo usan para saber si el servicio está activo.
    """
    return {"status": "ok", "service": "config-service"}
