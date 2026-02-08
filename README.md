# BDNS Portal

Portal público para consulta de subvenciones y ayudas de la Base de Datos Nacional de Subvenciones (BDNS) de España.

## 🎯 Descripción

Aplicación web que proporciona acceso público a datos de convocatorias y concesiones de subvenciones mediante una interfaz GraphQL moderna y un frontend Vue3 intuitivo.

**Modo de operación:** Solo lectura (los datos son actualizados por `bdns_etl`)

## 🏗️ Arquitectura

```
bdns_portal/
├── backend/           # API GraphQL (FastAPI + Strawberry)
│   ├── src/
│   │   └── bdns_portal/
│   ├── alembic/      # Migraciones DB
│   └── main.py
└── frontend/          # UI Vue3
    ├── src/
    │   ├── views/
    │   └── components/
    └── package.json
```

## 🚀 Stack Tecnológico

### Backend
- FastAPI + Strawberry GraphQL
- SQLAlchemy 2.0 + PostgreSQL 16
- Redis (caché)
- Puerto: 8000

### Frontend
- Vue 3 + Vite
- TailwindCSS
- graphql-request
- Chart.js
- Puerto: 3000

## 🔧 Instalación Rápida

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e .
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📚 Documentación de API

GraphQL Playground: http://localhost:8000/graphql

**Ejemplo de query:**
```graphql
query {
  convocatorias(limit: 10) {
    id
    codigo_bdns
    descripcion
    organo {
      nombre
    }
  }
}
```

## 🔗 Enlaces

- **Backend GraphQL:** http://localhost:8000/graphql
- **Frontend:** http://localhost:3000
- **Health check:** http://localhost:8000/health

## 📝 Notas

- **Autenticación:** No requerida (público)
- **Caché:** Redis con TTL de 1 hora
- **BD:** PostgreSQL compartida con `bdns_etl`
- **Modo:** Solo lectura

---

**Versión:** 1.0.0
