# culturalroute-ai-config

## ¿Qué hace este servicio?
El **Config Service** centraliza todos los parámetros configurables del sistema CulturalRoute AI. Permite que otros microservicios consulten y ajusten valores operativos (como pesos del scoring o radios de búsqueda) sin necesidad de modificar el código fuente.

## Sprint 1 - Historia S1-H8
**Dev asignado:** D8  
**Criterio de aceptación:** Config accesible vía API

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/config` | Lista todos los parámetros |
| GET | `/config/{key}` | Obtiene un parámetro por clave |
| POST | `/config` | Crea un nuevo parámetro |
| PATCH | `/config/{key}` | Actualiza el valor de un parámetro |
| GET | `/health` | Verifica que el servicio está activo |

## Variables de entorno
```
DATABASE_URL=postgresql://config_user:config_pass@localhost:5432/config_db
```

## Cómo ejecutar localmente
```bash
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el servicio
uvicorn app.main:app --reload --port 8007
```

## Documentación interactiva
Una vez corriendo, abrí en el navegador:
```
http://localhost:8007/docs
```

## Base de datos
- **Nombre:** config_db
- **Tabla:** config_parameters
- **Motor:** PostgreSQL

## Parámetros iniciales cargados automáticamente
| Clave | Valor por defecto | Descripción |
|-------|-------------------|-------------|
| scoring_weight_quality | 0.3 | Peso calidad de datos en scoring |
| scoring_weight_cultural_relevance | 0.4 | Peso relevancia cultural en scoring |
| scoring_weight_accessibility | 0.3 | Peso accesibilidad en scoring |
| geo_nearby_radius_km | 5.0 | Radio de búsqueda de lugares cercanos (km) |
| route_max_places | 5 | Máximo de lugares por ruta sugerida |
