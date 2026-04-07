# ============================================================
# MAIN - Punto de entrada del BFF
# Crea la aplicación FastAPI, registra las rutas
# y define el health check requerido por el proyecto.
# El BFF no inicializa base de datos porque no tiene una propia.
# ============================================================

from fastapi import FastAPI
from app.routers import bff

app = FastAPI(
    title="CulturalRoute AI – BFF / API Gateway",
    description=(
        "Backend for Frontend de CulturalRoute AI. "
        "Actúa como punto único de entrada para el frontend, "
        "agrega respuestas de múltiples microservicios "
        "y adapta los contratos para el consumo de la interfaz. "
        
    ),
    version="1.0.0"
)

# Registrar los endpoints del BFF
app.include_router(bff.router)


@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint de salud requerido por el proyecto.
    Docker y otros servicios lo usan para verificar que el BFF está activo.
    """
    return {"status": "ok", "service": "bff"}
