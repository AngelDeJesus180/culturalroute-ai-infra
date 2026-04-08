# ============================================================
# SCHEMAS - config.py
# Define los DTOs (Data Transfer Objects) de entrada y salida.
# Pydantic valida automáticamente que los datos tengan el formato correcto.
# Esta capa separa los objetos de transporte (API) del dominio.
# ============================================================

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ConfigParameterCreate(BaseModel):
    """
    DTO de entrada para crear un nuevo parámetro.
    El cliente debe enviar estos campos en el body del POST.
    """
    config_key: str = Field(..., example="scoring_weight_quality",
                            description="Clave única del parámetro")
    config_value: str = Field(..., example="0.3",
                              description="Valor del parámetro")
    description: Optional[str] = Field(None,
                                       example="Peso del criterio calidad de datos en el scoring")


class ConfigParameterUpdate(BaseModel):
    """
    DTO de entrada para actualizar un parámetro existente.
    Solo se envía el nuevo valor.
    """
    config_value: str = Field(..., example="0.5",
                              description="Nuevo valor del parámetro")


class ConfigParameterResponse(BaseModel):
    """
    DTO de salida: lo que el API devuelve al cliente.
    """
    id: str
    config_key: str
    config_value: str
    description: Optional[str]
    updated_at: datetime

    class Config:
        from_attributes = True  # Permite convertir desde objetos ORM
