# ============================================================
# CAPA DE DOMINIO - models.py
# Define las entidades que el BFF maneja internamente.
# No depende de FastAPI ni de bases de datos.
# El BFF no tiene BD propia, pero sí tiene modelos de dominio
# que representan la información que agrega de otros servicios.
# ============================================================

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class PlaceSummary:
    """
    Resumen de un lugar cultural tal como el BFF lo expone al frontend.
    Agrega datos del Place Service.
    """
    id: str
    name: str
    city: str
    category_id: str
    status: str
    short_description: Optional[str] = None
    address: Optional[str] = None
    source: Optional[str] = None

    def is_published(self) -> bool:
        """Regla de negocio: solo lugares publicados se exponen al frontend."""
        return self.status == "published"


@dataclass
class CatalogResponse:
    """
    Respuesta agregada del catálogo. Puede contener múltiples lugares.
    """
    total: int
    places: List[PlaceSummary] = field(default_factory=list)


@dataclass
class AssistantQuery:
    """
    Consulta del usuario al asistente inteligente.
    El BFF la recibe y la reenvía al AI Assistant Service.
    """
    question: str
    user_lat: Optional[float] = None
    user_lng: Optional[float] = None

    def is_valid(self) -> bool:
        """La pregunta no puede estar vacía."""
        return bool(self.question.strip())


@dataclass
class AssistantAnswer:
    """
    Respuesta del asistente que el BFF devuelve al frontend.
    Agrega la respuesta del AI Assistant Service.
    """
    interaction_id: str
    interpreted_intent: str
    answer_text: str
    sources: List[str] = field(default_factory=list)
