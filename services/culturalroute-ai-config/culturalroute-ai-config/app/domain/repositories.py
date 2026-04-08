# ============================================================
# CAPA DE DOMINIO - repositories.py
# Define el CONTRATO (interfaz) que debe cumplir cualquier
# repositorio de configuración. El dominio dice QUÉ operaciones
# necesita, sin saber CÓMO se guardan los datos.
# ============================================================

from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import ConfigParameter


class ConfigRepository(ABC):
    """
    Interfaz abstracta del repositorio de configuración.
    La capa de infraestructura implementará esto con SQLAlchemy + PostgreSQL.
    """

    @abstractmethod
    def get_all(self) -> List[ConfigParameter]:
        """Retorna todos los parámetros del sistema."""
        pass

    @abstractmethod
    def get_by_key(self, key: str) -> Optional[ConfigParameter]:
        """Busca un parámetro por su clave única."""
        pass

    @abstractmethod
    def create(self, param: ConfigParameter) -> ConfigParameter:
        """Guarda un nuevo parámetro en la base de datos."""
        pass

    @abstractmethod
    def update(self, key: str, new_value: str) -> Optional[ConfigParameter]:
        """Actualiza el valor de un parámetro existente."""
        pass
