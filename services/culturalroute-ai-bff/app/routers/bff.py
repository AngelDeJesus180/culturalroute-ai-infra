# ============================================================
# CAPA DE ROUTERS - bff.py
# Define los endpoints HTTP del BFF.
# Recibe requests, los delega al BFFService y devuelve respuestas.
# No contiene lógica de negocio: solo entrada/salida HTTP.
# ============================================================

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional

from app.infrastructure.http_clients import (
    PlaceServiceClient,
    AssistantServiceClient,
    ServiceUnavailableError
)
from app.application.bff_service import BFFService
from app.domain.models import AssistantQuery
from app.schemas.bff import (
    CatalogOut,
    PlaceSummaryOut,
    AssistantQueryIn,
    AssistantAnswerOut
)

router = APIRouter(tags=["BFF"])


def get_bff_service() -> BFFService:
    """
    Construye el BFFService con sus dependencias.
    FastAPI la llama automáticamente en cada request.
    """
    return BFFService(
        place_client=PlaceServiceClient(),
        assistant_client=AssistantServiceClient()
    )


@router.get(
    "/catalog",
    response_model=CatalogOut,
    summary="Obtener catálogo de lugares",
    description=(
        "Retorna el listado de lugares culturales disponibles. "
        "Agrega datos del Place Service y los adapta para el frontend."
    )
)
def get_catalog(service: BFFService = Depends(get_bff_service)):
    """
    GET /catalog
    Punto de entrada principal del frontend para explorar lugares.
    """
    try:
        result = service.get_catalog()
        return CatalogOut(
            total=result.total,
            places=[
                PlaceSummaryOut(
                    id=p.id,
                    name=p.name,
                    city=p.city,
                    category_id=p.category_id,
                    status=p.status,
                    short_description=p.short_description,
                    address=p.address
                )
                for p in result.places
            ]
        )
    except ServiceUnavailableError as e:
        raise HTTPException(
            status_code=503,
            detail={"error": "service_unavailable", "message": str(e)}
        )


@router.get(
    "/catalog/{place_id}",
    response_model=PlaceSummaryOut,
    summary="Obtener detalle de un lugar",
    description="Retorna la información detallada de un lugar cultural específico."
)
def get_place_detail(place_id: str, service: BFFService = Depends(get_bff_service)):
    """
    GET /catalog/{place_id}
    Usado por el frontend cuando el usuario hace clic en un lugar del catálogo.
    """
    try:
        place = service.get_place_detail(place_id)
    except ServiceUnavailableError as e:
        raise HTTPException(
            status_code=503,
            detail={"error": "service_unavailable", "message": str(e)}
        )

    if place is None:
        raise HTTPException(
            status_code=404,
            detail={
                "error": "not_found",
                "message": f"No se encontró un lugar con ID '{place_id}'"
            }
        )

    return PlaceSummaryOut(
        id=place.id,
        name=place.name,
        city=place.city,
        category_id=place.category_id,
        status=place.status,
        short_description=place.short_description,
        address=place.address
    )


@router.post(
    "/assistant/query",
    response_model=AssistantAnswerOut,
    summary="Consultar al asistente inteligente",
    description=(
        "Envía una pregunta al asistente y retorna una respuesta contextualizada. "
        "En Sprint 1 devuelve respuesta mock si el Assistant Service no está disponible."
    )
)
def query_assistant(body: AssistantQueryIn, service: BFFService = Depends(get_bff_service)):
    """
    POST /assistant/query
    El frontend lo usa para la funcionalidad de chat del asistente.
    """
    try:
        query = AssistantQuery(
            question=body.question,
            user_lat=body.user_lat,
            user_lng=body.user_lng
        )
        answer = service.query_assistant(query)
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"error": "validation_error", "message": str(e)}
        )
    except ServiceUnavailableError as e:
        raise HTTPException(
            status_code=503,
            detail={"error": "service_unavailable", "message": str(e)}
        )

    return AssistantAnswerOut(
        interaction_id=answer.interaction_id,
        interpreted_intent=answer.interpreted_intent,
        answer_text=answer.answer_text,
        sources=answer.sources
    )
