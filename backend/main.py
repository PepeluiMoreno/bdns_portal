"""
BDNS Portal - API GraphQL para consulta pública de subvenciones

Portal público de solo lectura para consultar datos de la
Base de Datos Nacional de Subvenciones (BDNS).
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from bdns_portal.graphql import graphql_schema as schema


# Crear app FastAPI
app = FastAPI(
    title="BDNS Portal API",
    description="API GraphQL pública para consultar subvenciones y ayudas públicas de España",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configurar orígenes específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    return {
        "service": "BDNS Portal API",
        "version": "1.0.0",
        "graphql": "/graphql",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "bdns-portal",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
