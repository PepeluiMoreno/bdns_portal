# BDNS Portal

Portal web publico para consulta y visualizacion de subvenciones de la Base de Datos Nacional de Subvenciones (BDNS). Backend GraphQL (FastAPI + Strawberry) y frontend interactivo (Vue 3) con dashboards, mapas y graficas.

**Modo de operacion:** Solo lectura. Los datos son cargados y actualizados por `bdns_etl`.

## Funcionalidades

- Consulta de convocatorias, concesiones y beneficiarios via GraphQL
- Dashboard interactivo con estadisticas por ano, region, tipo de beneficiario y organo
- Mapa interactivo de Espana con heatmap regional
- Graficas de evolucion temporal, distribucion por tipo y concentracion de ayudas
- Busqueda avanzada con filtros combinados y paginacion cursor-based (Relay)
- Cache Redis para consultas de agregacion
- Notificaciones Telegram

## Stack

| Componente | Tecnologia |
|---|---|
| Backend API | FastAPI + Strawberry GraphQL (puerto 8000) |
| Frontend | Vue 3 + Vite + TailwindCSS (puerto 3000) |
| Graficas | Chart.js + vue-chartjs |
| Mapas | D3-geo + TopoJSON + SVG |
| Cache | Redis 7 (TTL 1 hora) |
| Base de datos | PostgreSQL 15 |
| ORM | SQLAlchemy 2.0 + asyncpg |
| Dependencia core | bdns_core |

## Estructura

```
bdns_portal/
├── backend/
│   └── src/bdns_portal/
│       ├── main.py                     # Entrada FastAPI
│       ├── cache/
│       │   └── redis_cache.py          # Capa de cache Redis
│       ├── core/
│       │   └── config.py               # Configuracion
│       ├── graphql/
│       │   ├── schema.py               # Esquema GraphQL
│       │   ├── types/                  # Tipos GraphQL
│       │   │   ├── convocatoria.py
│       │   │   ├── beneficiario.py
│       │   │   ├── concesion.py
│       │   │   ├── catalogos.py
│       │   │   ├── estadisticas.py
│       │   │   └── pagination.py
│       │   ├── inputs/                 # Filtros de entrada
│       │   └── resolvers/              # Resolvers (queries a BD)
│       │       ├── convocatoria.py
│       │       ├── beneficiario.py
│       │       ├── concesion.py
│       │       ├── catalogos.py
│       │       └── estadisticas.py     # Agregaciones complejas
│       └── services/
│           └── telegram_notifications/
│
├── frontend/
│   └── src/
│       ├── App.vue
│       ├── components/
│       │   ├── Dashboard2.vue          # Dashboard principal
│       │   ├── SpainMap.vue            # Mapa interactivo de Espana
│       │   ├── RegionHeatmap.vue       # Heatmap regional
│       │   ├── RegionStatsTable.vue    # Tabla por comunidades
│       │   ├── BeneficiaryTypePieChart.vue
│       │   ├── TotalEvolutionChart.vue # Evolucion temporal
│       │   ├── ConvocatoriaSearch.vue  # Buscador
│       │   ├── ConvocatoriaDetail.vue  # Vista detalle
│       │   ├── ConvocatoriaFilter.vue
│       │   ├── ConcesionesPorBeneficiario.vue
│       │   └── InternationalBeneficiaries.vue
│       ├── services/
│       │   ├── graphql.js              # Cliente GraphQL
│       │   └── mockData.js             # Datos mock para desarrollo
│       └── utils/
│           └── regions.js              # Utilidades geograficas
│
├── Dockerfile
└── Dockerfile.frontend
```

## Inicio rapido

```bash
# Backend
cd backend
pip install -e .
uvicorn bdns_portal.main:app --reload  # http://localhost:8000

# Frontend
cd frontend
npm install
npm run dev                            # http://localhost:3000
```

## Endpoints

| URL | Descripcion |
|---|---|
| `/graphql` | GraphQL endpoint + Playground |
| `/docs` | Documentacion OpenAPI |
| `/health` | Health check general |
| `/health/redis` | Health check Redis |
| `/info` | Informacion del servicio |

## Ejemplos GraphQL

```graphql
# Convocatorias con paginacion Relay
query {
  convocatorias(first: 10, filtro: { year: 2024 }) {
    edges {
      node {
        codigoBdns
        titulo
        presupuesto
        organo { nombre }
      }
    }
    pageInfo { hasNextPage endCursor }
  }
}

# Estadisticas por region
query {
  estadisticasPorRegion(year: 2024) {
    region { nombre }
    totalConcesiones
    importeTotal
  }
}

# Buscar beneficiarios
query {
  beneficiarios(filtro: { nombre: "universidad" }, first: 5) {
    edges {
      node {
        nif
        nombre
        formaJuridica { descripcion }
      }
    }
  }
}
```

## Variables de entorno

```bash
DATABASE_URL=postgresql://user:pass@localhost:5432/bdns
REDIS_URL=redis://:password@localhost:6379/0
CORS_ORIGINS=http://localhost:3000
GRAPHQL_INTROSPECTION=true
GRAPHQL_PLAYGROUND=true
TELEGRAM_BOT_TOKEN=your-token
TELEGRAM_ENABLED=false
```

## Licencia

MIT
