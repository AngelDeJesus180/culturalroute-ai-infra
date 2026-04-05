# ============================================================
# CAPA DE INFRAESTRUCTURA - repositories.py
# Implementación concreta del repositorio usando SQLAlchemy.
# Aquí SÍ se sabe cómo se guardan los datos (PostgreSQL).
# Implementa el contrato definido en domain/repositories.py
# ============================================================

import uuid
from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.models import ConfigParameter
from app.domain.repositories import ConfigRepository
from app.infrastructure.database import ConfigParameterORM


class SQLConfigRepository(ConfigRepository):
    """
    Implementación del repositorio usando SQLAlchemy + PostgreSQL.
    Traduce entre objetos de dominio (ConfigParameter) y ORM (ConfigParameterORM).
    """

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ConfigParameter]:
        """Consulta todos los parámetros de la tabla."""
        rows = self.db.query(ConfigParameterORM).all()
        return [self._to_domain(row) for row in rows]

    def get_by_key(self, key: str) -> Optional[ConfigParameter]:
        """Busca un parámetro por su clave única."""
        row = self.db.query(ConfigParameterORM).filter(
            ConfigParameterORM.config_key == key
        ).first()
        return self._to_domain(row) if row else None

    def create(self, param: ConfigParameter) -> ConfigParameter:
        """Inserta un nuevo parámetro en la base de datos."""
        new_id = str(uuid.uuid4())
        row = ConfigParameterORM(
            id=new_id,
            config_key=param.config_key,
            config_value=param.config_value,
            description=param.description,
            updated_at=datetime.now(timezone.utc)
        )
        self.db.add(row)
        self.db.commit()
        self.db.refresh(row)
        return self._to_domain(row)

    def update(self, key: str, new_value: str) -> Optional[ConfigParameter]:
        """Actualiza el valor de un parámetro existente."""
        row = self.db.query(ConfigParameterORM).filter(
            ConfigParameterORM.config_key == key
        ).first()
        if not row:
            return None
        row.config_value = new_value
        row.updated_at = datetime.now(timezone.utc)
        self.db.commit()
        self.db.refresh(row)
        return self._to_domain(row)

    def _to_domain(self, row: ConfigParameterORM) -> ConfigParameter:
        """Convierte un objeto ORM en un objeto de dominio."""
        return ConfigParameter(
            id=row.id,
            config_key=row.config_key,
            config_value=row.config_value,
            description=row.description or "",
            updated_at=row.updated_at
        )
