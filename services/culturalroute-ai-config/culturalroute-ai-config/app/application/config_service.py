# ============================================================
# CAPA DE APLICACIÓN - config_service.py
# Orquesta los casos de uso del Config Service.
# Conecta la capa de entrada (routers) con el dominio y la infraestructura.
# Aquí vive la lógica del PROCESO, no del negocio puro.
# ============================================================

from typing import List, Optional
from datetime import datetime, timezone

from app.domain.models import ConfigParameter
from app.domain.repositories import ConfigRepository


class ConfigService:
    """
    Servicio de aplicación para gestionar parámetros de configuración.
    Recibe el repositorio por inyección de dependencias (no lo crea él solo).
    """

    def __init__(self, repository: ConfigRepository):
        self.repository = repository

    def get_all_parameters(self) -> List[ConfigParameter]:
        """
        Caso de uso: obtener todos los parámetros del sistema.
        Usado por el BFF y otros servicios para leer configuración central.
        """
        return self.repository.get_all()

    def get_parameter(self, key: str) -> Optional[ConfigParameter]:
        """
        Caso de uso: obtener un parámetro específico por su clave.
        Por ejemplo: GET /config/scoring_weight_quality
        """
        return self.repository.get_by_key(key)

    def create_parameter(self, key: str, value: str, description: str) -> ConfigParameter:
        """
        Caso de uso: registrar un nuevo parámetro configurable.
        Valida con la regla de dominio antes de guardar.
        """
        param = ConfigParameter(
            config_key=key,
            config_value=value,
            description=description,
            updated_at=datetime.now(timezone.utc)
        )
        if not param.is_valid():
            raise ValueError("La clave y el valor del parámetro no pueden estar vacíos.")
        return self.repository.create(param)

    def update_parameter(self, key: str, new_value: str) -> Optional[ConfigParameter]:
        """
        Caso de uso: actualizar el valor de un parámetro existente.
        Si el parámetro no existe, retorna None (el router decide qué responder).
        """
        if not new_value.strip():
            raise ValueError("El nuevo valor no puede estar vacío.")
        return self.repository.update(key, new_value)
