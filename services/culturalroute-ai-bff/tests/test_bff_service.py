# ============================================================
# TESTS - test_bff_service.py
# Prueba unitaria básica del BFFService.
# Usa mocks para no depender de servicios externos.
# Requerido por el Definition of Done del proyecto.
# ============================================================

import pytest
from unittest.mock import MagicMock
from app.application.bff_service import BFFService
from app.domain.models import AssistantQuery


def _make_service(places=None, assistant_response=None):
    """Helper: construye un BFFService con clientes mockeados."""
    place_client = MagicMock()
    place_client.get_all_places.return_value = places or []
    place_client.get_place_by_id.return_value = (
        places[0] if places else None
    )

    assistant_client = MagicMock()
    assistant_client.send_query.return_value = assistant_response or {
        "interaction_id": "test-001",
        "interpreted_intent": "general_query",
        "answer_text": "Respuesta de prueba",
        "sources": ["mock"]
    }

    return BFFService(place_client=place_client, assistant_client=assistant_client)


def test_get_catalog_returns_places():
    """El catálogo debe retornar los lugares del Place Service."""
    raw_places = [
        {
            "id": "uuid-001",
            "name": "Museo del Oro",
            "city": "Bogotá",
            "category_id": "cat-001",
            "status": "published",
            "short_description": "Museo arqueológico",
            "address": "Cra 6 #15-88"
        }
    ]
    service = _make_service(places=raw_places)
    result = service.get_catalog()

    assert result.total == 1
    assert result.places[0].name == "Museo del Oro"
    assert result.places[0].city == "Bogotá"


def test_get_catalog_empty():
    """El catálogo vacío no debe lanzar error."""
    service = _make_service(places=[])
    result = service.get_catalog()
    assert result.total == 0
    assert result.places == []


def test_get_place_detail_found():
    """Debe retornar el lugar cuando existe."""
    raw_places = [
        {
            "id": "uuid-001",
            "name": "Museo del Oro",
            "city": "Bogotá",
            "category_id": "cat-001",
            "status": "published"
        }
    ]
    service = _make_service(places=raw_places)
    place = service.get_place_detail("uuid-001")

    assert place is not None
    assert place.id == "uuid-001"


def test_get_place_detail_not_found():
    """Debe retornar None cuando el lugar no existe."""
    service = _make_service(places=None)
    place = service.get_place_detail("uuid-inexistente")
    assert place is None


def test_query_assistant_valid():
    """El asistente debe retornar una respuesta para una pregunta válida."""
    service = _make_service()
    query = AssistantQuery(question="¿Qué museos hay en Bogotá?")
    answer = service.query_assistant(query)

    assert answer.interaction_id == "test-001"
    assert answer.answer_text == "Respuesta de prueba"


def test_query_assistant_empty_question():
    """Una pregunta vacía debe lanzar ValueError."""
    service = _make_service()
    query = AssistantQuery(question="   ")

    with pytest.raises(ValueError):
        service.query_assistant(query)
