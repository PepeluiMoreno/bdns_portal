FROM python:3.11-slim

RUN groupadd -r bdns && useradd -r -g bdns bdns

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools wheel

COPY --from=bdns_core . /bdns_core
RUN pip install --no-cache-dir -e /bdns_core

COPY backend/pyproject.toml ./
COPY --chown=bdns:bdns backend/src ./src
RUN pip install --no-cache-dir -e .

USER bdns

CMD ["uvicorn", "bdns_portal.main:app", "--host", "0.0.0.0", "--port", "8000"]
