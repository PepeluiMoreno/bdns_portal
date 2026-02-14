#!/bin/bash
# run.sh - Arranca BDNS Portal API

set -e
cd "$(dirname "$0")"

# Activar entorno virtual
[ -d ".venv" ] && source .venv/bin/activate || source venv/bin/activate

# Añadir src al PYTHONPATH
export PYTHONPATH="$PWD/src:$PYTHONPATH"

# Obtener configuración desde bdns_core
SETTINGS=$(python -c "
from bdns_core.config import get_portal_settings;
s = get_portal_settings();
print(f'{s.HOST}:{s.PORT}:{s.ENVIRONMENT}:{s.WORKERS}')
")
HOST=$(echo $SETTINGS | cut -d: -f1)
PORT=$(echo $SETTINGS | cut -d: -f2)
ENVIRONMENT=$(echo $SETTINGS | cut -d: -f3)
WORKERS=$(echo $SETTINGS | cut -d: -f4)

# Construir comando
CMD="uvicorn bdns_portal.main:app --host $HOST --port $PORT"
[ "$ENVIRONMENT" = "development" ] && CMD="$CMD --reload --reload-dir src" || CMD="$CMD --workers $WORKERS"

# Ejecutar
exec $CMD