# ============================================================
# DOCKERFILE - Config Service
# Define cómo empaquetar el servicio en un contenedor Docker.
# ============================================================

# Imagen base de Python liviana
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar e instalar dependencias primero (mejor uso de caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Puerto en el que escucha el servicio
EXPOSE 8007

# Comando para iniciar el servicio con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8007"]
