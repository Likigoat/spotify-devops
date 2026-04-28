# ─── Dockerfile – Servicio Auxiliar SpotiDev ──────────────
# Contenedor 2: Servicio de monitoreo y estado del proyecto
# Puerto: 5001

FROM python:3.11-slim

# Metadatos
LABEL maintainer="SpotiDev DevOps Team"
LABEL description="Servicio auxiliar de monitoreo y diagnóstico"
LABEL version="1.0.0"

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5001

# Directorio de trabajo
WORKDIR /helper

# Copiar e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del servicio
COPY helper.py .

# Exponer puerto
EXPOSE 5001

# Usuario no-root
RUN adduser --disabled-password --gecos "" helperuser
USER helperuser

# Comando de inicio
CMD ["python", "helper.py"]