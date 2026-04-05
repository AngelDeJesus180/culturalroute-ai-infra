# ============================================================
# CAPA DE DOMINIO - models.py
# Aquí se define la entidad principal del negocio: ConfigParameter
# Esta clase NO depende de ninguna base de datos ni framework.
# Solo describe qué es un parámetro de configuración.
# ============================================================

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ConfigParameter:
    """
    Entidad de dominio que representa un parámetro configurable del sistema.

    Atributos:
        config_key   : nombre único del parámetro, ej: "scoring_weight_quality"
        config_value : valor del parámetro, puede ser número, texto o JSON
        description  : explicación en lenguaje natural de para qué sirve
        updated_at   : cuándo se actualizó por última vez
        id           : identificador único UUID (opcional al crear)
    """
    config_key: str
    config_value: str
    description: str
    updated_at: datetime
    id: Optional[str] = None

    def is_valid(self) -> bool:
        """
        Regla de negocio: un parámetro es válido si tiene clave y valor no vacíos.
        """
        return bool(self.config_key.strip()) and bool(self.config_value.strip())
