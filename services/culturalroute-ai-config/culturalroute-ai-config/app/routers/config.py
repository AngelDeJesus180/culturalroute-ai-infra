# ============================================================
# CAPA DE ROUTERS - config.py
# Define los endpoints HTTP del Config Service.
# Recibe requests, los delega al ConfigService y devuelve respuestas.
# No contiene lógica de negocio: solo entrada/salida HTTP.
# ============================================================

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.infrastructure.database import get_db
from app.infrastructure.repositories import SQLConfigRepository
from app.application.config_service import ConfigService
from app.schemas.config import (
    ConfigParameterCreate,
    ConfigParameterUpdate,
    ConfigParameterResponse
)

router = APIRouter(prefix="/config", tags=["Config"])


def get_service(db: Session = Depends(get_db)) -> ConfigService:
    """
    Función auxiliar que construye el ConfigService con sus dependencias.
    FastAPI la llama automáticamente en cada request.
    """
    repo = SQLConfigRepository(db)
    return ConfigService(repo)


@router.get(
    "/",
    response_model=List[ConfigParameterResponse],
    summary="Obtener todos los parámetros",
    description="Retorna la lista completa de parámetros configurables del sistema."
)
def get_all_config(service: ConfigService = Depends(get_service)):
    """
    GET /config
    Usado por otros microservicios (Analytics, Route) para leer
    parámetros como pesos del scoring o radio de cercanía.
    """
    return service.get_all_parameters()


@router.get(
    "/{key}",
    response_model=ConfigParameterResponse,
    summary="Obtener un parámetro por clave",
    description="Busca y retorna un parámetro específico según su clave única."
)
def get_config_by_key(key: str, service: ConfigService = Depends(get_service)):
    """
    GET /config/{key}
    Ejemplo: GET /config/scoring_weight_quality
    """
    param = service.get_parameter(key)
    if not param:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"No existe un parámetro con la clave '{key}'"
            }
        )
    return param


@router.post(
    "/",
    response_model=ConfigParameterResponse,
    status_code=201,
    summary="Crear un nuevo parámetro",
    description="Registra un nuevo parámetro configurable en el sistema."
)
def create_config(body: ConfigParameterCreate, service: ConfigService = Depends(get_service)):
    """
    POST /config
    Crea un parámetro nuevo. Si la clave ya existe, devuelve error 400.
    """
    try:
        return service.create_parameter(
            key=body.config_key,
            value=body.config_value,
            description=body.description or ""
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": "validation_error", "message": str(e)})


@router.patch(
    "/{key}",
    response_model=ConfigParameterResponse,
    summary="Actualizar valor de un parámetro",
    description="Modifica el valor de un parámetro existente sin necesidad de cambiar el código."
)
def update_config(key: str, body: ConfigParameterUpdate, service: ConfigService = Depends(get_service)):
    """
    PATCH /config/{key}
    Ejemplo: PATCH /config/scoring_weight_quality
    Body: { "config_value": "0.5" }
    """
    try:
        updated = service.update_parameter(key, body.config_value)
    except ValueError as e:
        raise HTTPException(status_code=400, detail={"error": "validation_error", "message": str(e)})

    if not updated:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"No existe un parámetro con la clave '{key}'"
            }
        )
    return updated
