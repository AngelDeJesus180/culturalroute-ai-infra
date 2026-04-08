# ============================================================
# CAPA DE APLICACIÓN - bff_service.py
# Orquesta los casos de uso del BFF.
# Recibe datos de los clientes HTTP, los transforma
# en modelos de dominio y los devuelve al router.
# ============================================================

from typing import List, Optional

from app.domain.models import (
    PlaceSummary,
    CatalogResponse,
    AssistantQuery,
    AssistantAnswer
)
from app.infrastructure.http_clients import (
    PlaceServiceClient,
    AssistantServiceClient,
    ServiceUnavailableError
)


class BFFService:
    """
    Servicio de aplicación del BFF.
    Agrega respuestas de múltiples microservicios
    y las adapta para el consumo del frontend.
    """

    def __init__(
        self,
        place_client: PlaceServiceClient,
        assistant_client: AssistantServiceClient
    ):
        self.place_client = place_client
        self.assistant_client = assistant_client

    def get_catalog(self) -> CatalogResponse:
        """
        Caso de uso: obtener el catálogo de lugares para el frontend.
        Llama al Place Service y filtra solo los lugares publicados.
        """
        raw_places = self.place_client.get_all_places()
        places = [self._map_to_place_summary(p) for p in raw_places]

        return CatalogResponse(
            total=len(places),
            places=places
        )

    def get_place_detail(self, place_id: str) -> Optional[PlaceSummary]:
        """
        Caso de uso: obtener el detalle de un lugar específico.
        Devuelve None si el lugar no existe.
        """
        raw = self.place_client.get_place_by_id(place_id)
        if raw is None:
            return None
        return self._map_to_place_summary(raw)

    def query_assistant(self, query: AssistantQuery) -> AssistantAnswer:
        """
        Caso de uso: enviar una pregunta al asistente inteligente.
        El BFF actúa como intermediario entre el frontend y el Assistant Service.
        """
        if not query.is_valid():
            raise ValueError("La pregunta no puede estar vacía.")

        raw = self.assistant_client.send_query(
            question=query.question,
            lat=query.user_lat,
            lng=query.user_lng
        )

        return AssistantAnswer(
            interaction_id=raw.get("interaction_id", "unknown"),
            interpreted_intent=raw.get("interpreted_intent", "unknown"),
            answer_text=raw.get("answer_text", ""),
            sources=raw.get("sources", [])
        )

    def _map_to_place_summary(self, raw: dict) -> PlaceSummary:
        """
        Convierte la respuesta cruda del Place Service
        en un modelo de dominio PlaceSummary.
        """
        return PlaceSummary(
            id=raw.get("id", ""),
            name=raw.get("name", ""),
            city=raw.get("city", ""),
            category_id=raw.get("category_id", ""),
            status=raw.get("status", "draft"),
            short_description=raw.get("short_description"),
            address=raw.get("address"),
            source=raw.get("source")
        )
