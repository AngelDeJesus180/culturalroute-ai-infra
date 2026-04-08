# ============================================================
# CAPA DE INFRAESTRUCTURA - http_clients.py
# Clientes HTTP para comunicarse con los microservicios internos.
# El BFF NO tiene base de datos propia.
# Su "infraestructura" son los clientes que llaman a otros servicios.
# ============================================================

import os
import httpx
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

# URLs de los microservicios internos (vienen de variables de entorno)
PLACE_SERVICE_URL = os.getenv("PLACE_SERVICE_URL", "http://localhost:8002")
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001")
ASSISTANT_SERVICE_URL = os.getenv("ASSISTANT_SERVICE_URL", "http://localhost:8008")

# Timeout en segundos para todas las llamadas HTTP
HTTP_TIMEOUT = 10.0


class PlaceServiceClient:
    """
    Cliente HTTP para el Place Service.
    Encapsula todas las llamadas al servicio de catálogo de lugares.
    """

    def __init__(self, base_url: str = PLACE_SERVICE_URL):
        self.base_url = base_url

    def get_all_places(self) -> List[Dict[str, Any]]:
        """
        Obtiene todos los lugares del catálogo.
        Llama a GET /places en el Place Service.
        """
        try:
            with httpx.Client(timeout=HTTP_TIMEOUT) as client:
                response = client.get(f"{self.base_url}/places")
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise ServiceUnavailableError(
                f"Place Service respondió con error {e.response.status_code}"
            )
        except httpx.RequestError:
            raise ServiceUnavailableError(
                "No se pudo conectar con el Place Service"
            )

    def get_place_by_id(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene un lugar específico por su ID.
        Llama a GET /places/{place_id} en el Place Service.
        """
        try:
            with httpx.Client(timeout=HTTP_TIMEOUT) as client:
                response = client.get(f"{self.base_url}/places/{place_id}")
                if response.status_code == 404:
                    return None
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise ServiceUnavailableError(
                f"Place Service respondió con error {e.response.status_code}"
            )
        except httpx.RequestError:
            raise ServiceUnavailableError(
                "No se pudo conectar con el Place Service"
            )


class AssistantServiceClient:
    """
    Cliente HTTP para el AI Assistant Service.
    Encapsula las llamadas al asistente inteligente.
    """

    def __init__(self, base_url: str = ASSISTANT_SERVICE_URL):
        self.base_url = base_url

    def send_query(self, question: str, lat: Optional[float], lng: Optional[float]) -> Dict[str, Any]:
        """
        Envía una pregunta al asistente.
        Llama a POST /assistant/query en el Assistant Service.
        """
        payload = {
            "question": question,
            "user_context": {}
        }
        if lat is not None and lng is not None:
            payload["user_context"] = {"lat": lat, "lng": lng}

        try:
            with httpx.Client(timeout=HTTP_TIMEOUT) as client:
                response = client.post(
                    f"{self.base_url}/assistant/query",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            raise ServiceUnavailableError(
                f"Assistant Service respondió con error {e.response.status_code}"
            )
        except httpx.RequestError:
            # En Sprint 1 el assistant puede no estar listo; devolvemos mock
            return _mock_assistant_response(question)


def _mock_assistant_response(question: str) -> Dict[str, Any]:
    """
    Respuesta mock del asistente para cuando el servicio aún no está disponible.
    Permite que el BFF funcione de forma autónoma en Sprint 1.
    """
    return {
        "interaction_id": "mock-interaction-001",
        "interpreted_intent": "general_query",
        "answer_text": (
            f"[MOCK - Sprint 1] Recibí tu pregunta: '{question}'. "
            "El AI Assistant Service estará disponible en Sprint 2."
        ),
        "sources": ["mock"]
    }


class ServiceUnavailableError(Exception):
    """Se lanza cuando un microservicio no está disponible o responde con error."""
    pass
