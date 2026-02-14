# Dockerfile para Backend (FastAPI)
FROM python:3.13-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de configuración
COPY packages/bdns_core/pyproject.toml /app/packages/bdns_core/
COPY apps/backend/pyproject.toml /app/backend/

# Instalar paquetes Python
COPY packages/bdns_core /app/packages/bdns_core
RUN pip install --no-cache-dir -e /app/packages/bdns_core

COPY apps/backend /app/backend
RUN pip install --no-cache-dir -e /app/backend

# Copiar scripts
COPY scripts /app/scripts

# Exponer puerto
EXPOSE 8001

# Punto de entrada
CMD ["uvicorn", "bdns_api.server:app", "--host", "0.0.0.0", "--port", "8001"]
