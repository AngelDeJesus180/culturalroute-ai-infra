# ============================================================
# SCHEMAS - bff.py
# DTOs (Data Transfer Objects) del BFF.
# Pydantic valida automáticamente que los datos del request
# tengan el formato correcto antes de llegar a la aplicación.
# ============================================================

from pydantic import BaseModel, Field
from typing import Optional, List


# ─────────────────────────────────────────
# Schemas de SALIDA (respuestas al frontend)
# ─────────────────────────────────────────

class PlaceSummaryOut(BaseModel):
    """
    Datos de un lugar cultural que el BFF devuelve al frontend.
    Solo expone los campos que el frontend necesita ver.
    """
    id: str
    name: str
    city: str
    category_id: str
    status: str
    short_description: Optional[str] = None
    address: Optional[str] = None

    class Config:
        from_attributes = True


class CatalogOut(BaseModel):
    """
    Respuesta del endpoint GET /catalog.
    Lista de lugares con total.
    """
    total: int
    places: List[PlaceSummaryOut]


# ─────────────────────────────────────────
# Schemas de ENTRADA (requests del frontend)
# ─────────────────────────────────────────

class AssistantQueryIn(BaseModel):
    """
    Body del POST /assistant/query.
    El frontend envía la pregunta y opcionalmente la ubicación del usuario.
    """
    question: str = Field(
        ...,
        min_length=1,
        example="¿Qué lugares culturales puedo visitar cerca?",
        description="Pregunta del usuario al asistente"
    )
    user_lat: Optional[float] = Field(
        None,
        example=4.6097,
        description="Latitud del usuario (opcional)"
    )
    user_lng: Optional[float] = Field(
        None,
        example=-74.0817,
        description="Longitud del usuario (opcional)"
    )


# ─────────────────────────────────────────
# Schemas de SALIDA para el asistente
# ─────────────────────────────────────────

class AssistantAnswerOut(BaseModel):
    """
    Respuesta del endpoint POST /assistant/query.
    """
    interaction_id: str
    interpreted_intent: str
    answer_text: str
    sources: List[str]


# ─────────────────────────────────────────
# Schema de ERROR estándar
# ─────────────────────────────────────────

class ErrorOut(BaseModel):
    """
    Estructura de error consistente para todos los endpoints del BFF.
    Todos los errores siguen este formato para facilitar manejo en el frontend.
    """
    error: str = Field(..., example="not_found")
    message: str = Field(..., example="No se encontró el lugar solicitado")
