# ============================================================
# CAPA DE INFRAESTRUCTURA - database.py
# Configura la conexión a PostgreSQL usando SQLAlchemy.
# También define el modelo ORM (la tabla real en la base de datos).
# ============================================================

import os
from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

# URL de conexión a la base de datos (viene de variable de entorno)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://config_user:config_pass@localhost:5432/config_db"
)

# Motor de SQLAlchemy: maneja la conexión real con PostgreSQL
engine = create_engine(DATABASE_URL)

# Fábrica de sesiones: cada request de la API abre y cierra su propia sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para todos los modelos ORM
Base = declarative_base()


class ConfigParameterORM(Base):
    """
    Modelo ORM: representa la tabla 'config_parameters' en config_db.
    Cada fila es un parámetro configurable del sistema.
    """
    __tablename__ = "config_parameters"

    id = Column(String, primary_key=True)           # UUID como texto
    config_key = Column(String, unique=True, nullable=False)   # clave única
    config_value = Column(String, nullable=False)              # valor del parámetro
    description = Column(String, nullable=True)                # para qué sirve
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


def get_db():
    """
    Generador de sesión de base de datos.
    FastAPI lo usa como dependencia (Depends) en cada endpoint.
    Garantiza que la sesión se cierre aunque haya errores.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Crea las tablas en la base de datos si no existen."""
    Base.metadata.create_all(bind=engine)
