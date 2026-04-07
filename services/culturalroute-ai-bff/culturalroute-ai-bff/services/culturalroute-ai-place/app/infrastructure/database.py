from sqlalchemy import create_engine, Column, String, Text, Float, DateTime, Enum, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv
import enum

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:Ajp64572314.@localhost:3306/place_db")

print(f"🔍 Conectando a: {DATABASE_URL}")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  # <--- ESTO FALTABA


class PlaceStatusDB(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    INACTIVE = "inactive"


class PlaceORM(Base):
    __tablename__ = "places"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    address = Column(String(255), nullable=True)
    latitude = Column(DECIMAL(10, 8), default=0)
    longitude = Column(DECIMAL(11, 8), default=0)
    rating = Column(DECIMAL(3, 2), default=0)
    status = Column(String(20), default="draft")  # Cambiado a String
    source = Column(String(100), default="manual")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()