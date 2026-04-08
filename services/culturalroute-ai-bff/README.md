# BFF / API Gateway – CulturalRoute AI
**Dev9 – Sprint 1**

## ¿Qué hace este servicio?

El BFF (Backend for Frontend) es el punto único de entrada para el frontend.
No contiene lógica de negocio: agrega respuestas de los microservicios internos
y adapta los contratos para que el frontend los consuma fácilmente.

## Endpoints disponibles (Sprint 1)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/health` | Verificar que el servicio está activo |
| GET | `/catalog` | Obtener catálogo de lugares culturales |
| GET | `/catalog/{place_id}` | Obtener detalle de un lugar específico |
| POST | `/assistant/query` | Consultar al asistente inteligente |

## Ejemplo de uso

**GET /catalog**
```bash
curl http://localhost:8009/catalog
```
Respuesta:
```json
{
  "total": 3,
  "places": [
    {
      "id": "uuid-001",
      "name": "Museo del Oro",
      "city": "Bogotá",
      "category_id": "cat-001",
      "status": "published"
    }
  ]
}
```

**POST /assistant/query**
```bash
curl -X POST http://localhost:8009/assistant/query \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Qué museos puedo visitar?", "user_lat": 4.6097, "user_lng": -74.0817}'
```

## Variables de entorno

Copia `.env.example` como `.env` y ajusta las URLs:

```bash
cp .env.example .env
```

| Variable | Descripción | Default |
|----------|-------------|---------|
| `PLACE_SERVICE_URL` | URL del Place Service | `http://localhost:8002` |
| `AUTH_SERVICE_URL` | URL del Auth Service | `http://localhost:8001` |
| `ASSISTANT_SERVICE_URL` | URL del Assistant Service | `http://localhost:8008` |

## Cómo ejecutar localmente

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar variables de entorno
cp .env.example .env

# 3. Iniciar el servicio
uvicorn app.main:app --host 0.0.0.0 --port 8009 --reload

# 4. Ver documentación interactiva
# Abrir http://localhost:8009/docs
```

## Cómo ejecutar con Docker

```bash
docker build -t bff-service .
docker run -p 8009:8009 --env-file .env bff-service
```

## Cómo ejecutar las pruebas

```bash
pip install pytest
pytest tests/ -v
```

## Arquitectura interna

```
app/
├── routers/bff.py          → Endpoints HTTP (entrada/salida)
├── application/bff_service.py → Casos de uso (lógica del proceso)
├── domain/models.py        → Entidades de negocio (sin frameworks)
├── infrastructure/http_clients.py → Clientes HTTP a otros servicios
├── schemas/bff.py          → DTOs Pydantic (validación)
└── main.py                 → Punto de entrada FastAPI
```

## Nota Sprint 1

El BFF funciona de forma autónoma. Si el Assistant Service no está disponible,
devuelve una respuesta mock claramente marcada. El Place Service sí debe estar
corriendo para que `/catalog` funcione con datos reales.
