# ─── Dockerfile – Aplicación Principal SpotiDev ───────────
# Contenedor 1: Flask app principal
# Puerto: 5000

FROM python:3.11-slim

# Metadatos
LABEL maintainer="SpotiDev DevOps Team"
LABEL description="Aplicación principal Flask de SpotiDev"
LABEL version="1.0.0"

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_ENV=production \
    PORT=5000

# Directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias primero (aprovecha caché de Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app.py .

# Exponer puerto
EXPOSE 5000

# Usuario no-root por seguridad
RUN adduser --disabled-password --gecos "" appuser
USER appuser

# Comando de inicio
CMD ["python", "app.py"]