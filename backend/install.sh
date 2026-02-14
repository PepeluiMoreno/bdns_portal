#!/bin/bash
# install.sh - Instala bdns_portal con dependencia local bdns_core

set -e

cd "$(dirname "$0")"

echo "📦 Instalando BDNS Portal API..."

# Crear entorno virtual si no existe
if [ ! -d "venv" ] && [ ! -d ".venv" ]; then
    echo "🔧 Creando entorno virtual..."
    python -m venv .venv
fi

# Activar entorno virtual
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    source venv/bin/activate
fi

# Instalar pip en última versión
pip install --upgrade pip

# Instalar bdns_core desde ruta relativa
echo "📚 Instalando bdns_core (local)..."
pip install -e ../../bdns_core

# Instalar bdns_portal
echo "🚀 Instalando bdns_portal..."
pip install -e .

echo "✅ Instalación completada"
echo ""
echo "👉 Para arrancar: ./run.sh"