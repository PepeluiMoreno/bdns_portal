"""
BDNS Portal - API GraphQL para consulta pública de subvenciones.

Portal público de solo lectura para consultar datos de la
Base de Datos Nacional de Subvenciones (BDNS).

Usa configuración centralizada de bdns_core.
"""
import logging
import time
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

from bdns_portal.graphql import graphql_schema as schema
from bdns_portal.cache.redis_cache import redis_cache
from bdns_core.config import get_portal_settings
from bdns_core.logging import get_logger


# Cargar settings
settings = get_portal_settings()

# Logger
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Maneja el ciclo de vida de la aplicación.
    - Startup: Inicializa conexiones (Redis)
    - Shutdown: Cierra conexiones correctamente
    """
    # ----- STARTUP -----
    logger.info("Iniciando BDNS Portal API...")
    
    # Inicializar Redis cache
    try:
        await redis_cache.init()
        logger.info("Redis cache conectado", extra={"redis_url": settings.REDIS_URL})
    except Exception as e:
        logger.error("Error conectando Redis", exc_info=e, extra={"redis_url": settings.REDIS_URL})
        # No fallamos el startup, Redis puede no estar disponible
        pass
    
    logger.info("Entorno: %s", settings.ENVIRONMENT)
    logger.info("GraphQL Playground: %s", "activado" if settings.GRAPHQL_PLAYGROUND else "desactivado")
    logger.info("BDNS Portal API listo")
    
    yield
    
    # ----- SHUTDOWN -----
    logger.info("Cerrando BDNS Portal API...")
    
    # Cerrar Redis
    if redis_cache.client:
        try:
            await redis_cache.client.close()
            logger.info("Redis cache cerrado")
        except Exception as e:
            logger.error("Error cerrando Redis", exc_info=e)


# Variable para timestamp de inicio
import_time = time.strftime("%Y-%m-%d %H:%M:%S")

# Crear app FastAPI con lifespan
app = FastAPI(
    title="BDNS Portal API",
    description="API GraphQL pública para consultar subvenciones y ayudas públicas de España",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.DEBUG,
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL
graphql_app = GraphQLRouter(
    schema,
    graphiql=settings.GRAPHQL_PLAYGROUND,
)
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root():
    """Root endpoint con información del servicio."""
    logger.debug("Root endpoint accedido")
    return {
        "service": "BDNS Portal API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "graphql": "/graphql",
        "docs": "/docs",
        "redoc": "/redoc",
        "health": "/health",
        "status": "operational"
    }


@app.get("/health")
async def health():
    """Health check endpoint para monitoreo."""
    # Verificar Redis
    redis_status = "ok" if redis_cache.client else "disconnected"
    
    logger.debug("Health check accedido", extra={"redis_status": redis_status})
    
    return {
        "status": "ok",
        "service": "bdns-portal",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "timestamp": import_time,
        "checks": {
            "redis": redis_status,
            "database": "ok",  # La DB se verifica por conexión
        }
    }


@app.get("/health/redis")
async def health_redis():
    """Health check específico de Redis."""
    if not redis_cache.client:
        logger.warning("Health check Redis: no conectado")
        return {
            "status": "error",
            "service": "redis",
            "message": "Redis no conectado"
        }
    
    try:
        await redis_cache.client.ping()
        logger.debug("Health check Redis: ok")
        return {
            "status": "ok",
            "service": "redis",
            "message": "Redis conectado y operativo"
        }
    except Exception as e:
        logger.error("Health check Redis: error", exc_info=e)
        return {
            "status": "error",
            "service": "redis",
            "message": str(e)
        }


@app.get("/info")
async def info():
    """Información detallada del servicio."""
    logger.debug("Info endpoint accedido")
    return {
        "service": "BDNS Portal API",
        "description": "Portal público de consulta de la Base de Datos Nacional de Subvenciones",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG,
        "documentation": {
            "graphql": "/graphql",
            "graphql_playground": settings.GRAPHQL_PLAYGROUND,
            "openapi": "/docs",
            "redoc": "/redoc"
        },
        "features": [
            "Convocatorias con paginación Relay",
            "Beneficiarios y pseudónimos",
            "Concesiones con importes nominales y equivalentes",
            "Catálogos completos (órganos, regiones, sectores, etc.)",
            "Estadísticas agregadas con cache Redis",
            "Sistema de notificaciones"
        ],
        "source": "https://github.com/pepelui/bdns",
        "contact": "joseluis.morgomez@gmail.com",
        "startup_time": import_time
    }


if __name__ == "__main__":
    import uvicorn
    
    log_level = "debug" if settings.DEBUG else "info"
    logger.info("Iniciando servidor Uvicorn", extra={
        "host": settings.HOST,
        "port": settings.PORT,
        "reload": settings.DEBUG,
        "workers": 1 if settings.DEBUG else settings.WORKERS,
        "log_level": log_level
    })
    
    uvicorn.run(
        "bdns_portal.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1 if settings.DEBUG else settings.WORKERS,
        log_level=log_level
    )