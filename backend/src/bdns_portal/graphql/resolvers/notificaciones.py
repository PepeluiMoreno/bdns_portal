"""
Resolvers GraphQL para el sistema de notificaciones.

Queries y Mutations para gestionar usuarios, suscripciones y el query builder.
"""
# graphql/resolvers/notificaciones.py
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from bdns_core.db.models import Usuario, SubscripcionNotificacion, EjecucionNotificacion
from ..types.notificaciones import (
    Usuario as UsuarioType,
    Suscripcion as SuscripcionType,
    Ejecucion as EjecucionType,
    TelegramLink,
    FilterDefinition,
    FilterOption,
    FieldDefinition,
    QueryPreview,
    TestResult,
    EntidadesDisponibles,
)


# ==================== CONVERSORES ====================

def _usuario_to_type(u) -> UsuarioType:
    return UsuarioType(
        id=u.id,
        email=u.email,
        nombre=u.nombre,
        telegram_chat_id=u.telegram_chat_id,
        telegram_username=u.telegram_username,
        telegram_verificado=u.telegram_verificado,
        activo=u.activo,
        created_at=u.created_at,
    )


def _suscripcion_to_type(s) -> SuscripcionType:
    return SuscripcionType(
        id=s.id,
        usuario_id=s.usuario_id,
        nombre=s.nombre,
        descripcion=s.descripcion,
        graphql_query=s.graphql_query,
        campo_id=s.campo_id,
        campos_comparar=s.campos_comparar,
        frecuencia=s.frecuencia,
        hora_preferida=s.hora_preferida,
        activo=s.activo,
        pausado_por_errores=s.pausado_por_errores,
        errores_consecutivos=s.errores_consecutivos,
        ultimo_error=s.ultimo_error,
        last_check=s.last_check,
        last_check_count=s.last_check_count,
        proxima_ejecucion=s.proxima_ejecucion,
        created_at=s.created_at,
    )


def _ejecucion_to_type(e) -> EjecucionType:
    return EjecucionType(
        id=e.id,
        subscripcion_id=e.subscripcion_id,
        fecha_ejecucion=e.fecha_ejecucion,
        estado=e.estado,
        registros_actuales=e.registros_actuales,
        registros_anteriores=e.registros_anteriores,
        nuevos=e.nuevos,
        modificados=e.modificados,
        eliminados=e.eliminados,
        notificacion_enviada=e.notificacion_enviada,
        error=e.error,
        created_at=e.created_at,
    )


# ==================== QUERIES: USUARIOS ====================

async def get_usuarios(
    info,
    activo: Optional[bool] = None,
    limite: int = 100,
    offset: int = 0
) -> List[UsuarioType]:
    db = info.context["db"]
    
    stmt = select(Usuario)
    if activo is not None:
        stmt = stmt.where(Usuario.activo == activo)
    
    stmt = stmt.offset(offset).limit(limite)
    result = await db.execute(stmt)
    usuarios = result.scalars().all()
    
    return [_usuario_to_type(u) for u in usuarios]


async def get_usuario(
    info,
    id: UUID
) -> Optional[UsuarioType]:
    db = info.context["db"]
    
    stmt = select(Usuario).where(Usuario.id == id)
    result = await db.execute(stmt)
    u = result.scalar_one_or_none()
    
    return _usuario_to_type(u) if u else None


async def get_usuario_por_email(
    info,
    email: str
) -> Optional[UsuarioType]:
    db = info.context["db"]
    
    stmt = select(Usuario).where(Usuario.email == email)
    result = await db.execute(stmt)
    u = result.scalar_one_or_none()
    
    return _usuario_to_type(u) if u else None


# ==================== QUERIES: SUSCRIPCIONES ====================

async def get_suscripciones(
    info,
    usuario_id: Optional[UUID] = None,
    activo: Optional[bool] = None,
    limite: int = 100,
    offset: int = 0
) -> List[SuscripcionType]:
    db = info.context["db"]
    
    stmt = select(SubscripcionNotificacion)
    if usuario_id is not None:
        stmt = stmt.where(SubscripcionNotificacion.usuario_id == usuario_id)
    if activo is not None:
        stmt = stmt.where(SubscripcionNotificacion.activo == activo)
    
    stmt = stmt.order_by(SubscripcionNotificacion.created_at.desc()).offset(offset).limit(limite)
    result = await db.execute(stmt)
    subs = result.scalars().all()
    
    return [_suscripcion_to_type(s) for s in subs]


async def get_suscripcion(
    info,
    id: UUID
) -> Optional[SuscripcionType]:
    db = info.context["db"]
    
    stmt = select(SubscripcionNotificacion).where(SubscripcionNotificacion.id == id)
    result = await db.execute(stmt)
    s = result.scalar_one_or_none()
    
    return _suscripcion_to_type(s) if s else None


# ==================== QUERIES: EJECUCIONES ====================

async def get_ejecuciones(
    info,
    subscripcion_id: Optional[UUID] = None,
    estado: Optional[str] = None,
    limite: int = 100,
    offset: int = 0
) -> List[EjecucionType]:
    db = info.context["db"]
    
    stmt = select(EjecucionNotificacion)
    if subscripcion_id is not None:
        stmt = stmt.where(EjecucionNotificacion.subscripcion_id == subscripcion_id)
    if estado is not None:
        stmt = stmt.where(EjecucionNotificacion.estado == estado)
    
    stmt = stmt.order_by(EjecucionNotificacion.fecha_ejecucion.desc()).offset(offset).limit(limite)
    result = await db.execute(stmt)
    ejecs = result.scalars().all()
    
    return [_ejecucion_to_type(e) for e in ejecs]


# ==================== QUERIES: QUERY BUILDER ====================

async def get_entidades_disponibles(info) -> EntidadesDisponibles:
    from telegram_notifications.query_builder import QueryBuilder
    
    return EntidadesDisponibles(
        entities=list(QueryBuilder.ENTITIES.keys()),
        default="concesiones"
    )


async def get_filtros_disponibles(
    info,
    entity: str
) -> List[FilterDefinition]:
    from telegram_notifications.query_builder import QueryBuilder

    if entity not in QueryBuilder.ENTITIES:
        return []

    filtros = QueryBuilder.get_available_filters(entity)
    result = []
    
    for f in filtros:
        options = None
        if f.get("options"):
            options = [FilterOption(value=o["value"], label=o["label"]) for o in f["options"]]
        
        result.append(FilterDefinition(
            name=f["name"],
            label=f["label"],
            type=f["type"],
            options=options,
            description=f.get("description"),
            ejemplo=f.get("ejemplo"),
            graphql_param=f.get("graphql_param"),
        ))
    
    return result


async def get_campos_disponibles(
    info,
    entity: str
) -> List[FieldDefinition]:
    from telegram_notifications.query_builder import QueryBuilder

    if entity not in QueryBuilder.ENTITIES:
        return []

    campos = QueryBuilder.get_available_fields(entity)
    return [FieldDefinition(name=k, description=v) for k, v in campos.items()]


async def preview_query(
    info,
    entity: str,
    filters: dict,
    fields: Optional[List[str]] = None,
    limite: int = 1000
) -> QueryPreview:
    from telegram_notifications.query_builder import QueryBuilder

    builder = QueryBuilder(entity=entity, limite=limite)

    for key, value in (filters or {}).items():
        if value is not None and value != "":
            builder.add_filter(key, value)

    if fields:
        builder.select_fields(fields)

    preview = builder.preview()
    
    return QueryPreview(
        query=preview["query"],
        entity=preview["entity"],
        filters_active=preview["filters_active"],
        fields_selected=preview["fields_selected"],
        fields=preview["fields"],
    )


async def test_query(
    info,
    entity: str,
    filters: dict,
    fields: Optional[List[str]] = None,
    limite: int = 100
) -> TestResult:
    import time
    from telegram_notifications.query_builder import QueryBuilder
    from telegram_notifications.monitor import execute_graphql_query, extract_records

    builder = QueryBuilder(entity=entity, limite=min(limite, 100))

    for key, value in (filters or {}).items():
        if value is not None and value != "":
            builder.add_filter(key, value)

    if fields:
        builder.select_fields(fields)

    query = builder.build()

    start = time.time()
    data, error = execute_graphql_query(query)
    duration_ms = (time.time() - start) * 1000

    if error:
        return TestResult(
            registros=0,
            primeros_registros=[],
            query_ejecutada=query,
            duracion_ms=round(duration_ms, 2),
            error=error
        )

    records = extract_records(data, "id")

    return TestResult(
        registros=len(records),
        primeros_registros=list(records.values())[:10],
        query_ejecutada=query,
        duracion_ms=round(duration_ms, 2),
    )


# ==================== MUTATIONS: USUARIOS ====================

async def crear_usuario(
    info,
    email: str,
    nombre: Optional[str] = None
) -> UsuarioType:
    db = info.context["db"]
    
    # Verificar email unico
    stmt = select(Usuario).where(Usuario.email == email)
    result = await db.execute(stmt)
    if result.scalar_one_or_none():
        raise ValueError(f"Email {email} ya registrado")

    u = Usuario(
        email=email,
        nombre=nombre,
        username=email.split('@')[0],  # Temporal hasta que tengas registro completo
        hashed_password="",  # La auth va en otro módulo
        role="user",
        activo=True
    )
    
    db.add(u)
    await db.commit()
    await db.refresh(u)
    
    return _usuario_to_type(u)


async def actualizar_usuario(
    info,
    id: UUID,
    email: Optional[str] = None,
    nombre: Optional[str] = None,
    activo: Optional[bool] = None
) -> Optional[UsuarioType]:
    db = info.context["db"]
    
    stmt = select(Usuario).where(Usuario.id == id)
    result = await db.execute(stmt)
    u = result.scalar_one_or_none()
    
    if not u:
        return None

    if email is not None:
        u.email = email
    if nombre is not None:
        u.nombre = nombre
    if activo is not None:
        u.activo = activo

    await db.commit()
    await db.refresh(u)
    
    return _usuario_to_type(u)


async def eliminar_usuario(
    info,
    id: UUID
) -> bool:
    db = info.context["db"]
    
    stmt = select(Usuario).where(Usuario.id == id)
    result = await db.execute(stmt)
    u = result.scalar_one_or_none()
    
    if not u:
        return False
    
    await db.delete(u)
    await db.commit()
    
    return True


async def generar_link_telegram(
    info,
    usuario_id: UUID
) -> Optional[TelegramLink]:
    import secrets
    from datetime import datetime, timedelta
    
    db = info.context["db"]
    
    stmt = select(Usuario).where(Usuario.id == usuario_id)
    result = await db.execute(stmt)
    u = result.scalar_one_or_none()
    
    if not u:
        return None

    token = secrets.token_urlsafe(32)
    u.telegram_token_verificacion = token
    u.telegram_token_expira = datetime.utcnow() + timedelta(hours=24)
    u.telegram_verificado = False
    
    await db.commit()

    return TelegramLink(
        usuario_id=usuario_id,
        token=token,
        url=f"https://t.me/BDNS_NotificadorBot?start={token}",
        expires_at=u.telegram_token_expira,
        instrucciones=f"Envía /vincular {token} al bot @BDNS_NotificadorBot"
    )


# ==================== MUTATIONS: SUSCRIPCIONES ====================

async def crear_suscripcion(
    info,
    usuario_id: UUID,
    nombre: str,
    graphql_query: str,
    descripcion: Optional[str] = None,
    campo_id: str = "id",
    campos_comparar: Optional[List[str]] = None,
    frecuencia: str = "semanal",
    hora_preferida: int = 8
) -> Optional[SuscripcionType]:
    db = info.context["db"]
    
    # Verificar usuario
    stmt = select(Usuario).where(Usuario.id == usuario_id)
    result = await db.execute(stmt)
    if not result.scalar_one_or_none():
        return None

    s = SubscripcionNotificacion(
        usuario_id=usuario_id,
        nombre=nombre,
        descripcion=descripcion,
        graphql_query=graphql_query,
        campo_id=campo_id,
        campos_comparar=campos_comparar,
        frecuencia=frecuencia,
        hora_preferida=hora_preferida,
    )
    
    db.add(s)
    await db.commit()
    await db.refresh(s)
    
    return _suscripcion_to_type(s)


async def crear_suscripcion_desde_builder(
    info,
    usuario_id: UUID,
    nombre: str,
    entity: str,
    filters: dict,
    descripcion: Optional[str] = None,
    fields: Optional[List[str]] = None,
    limite: int = 1000,
    frecuencia: str = "semanal",
    hora_preferida: int = 8
) -> Optional[SuscripcionType]:
    from telegram_notifications.query_builder import QueryBuilder
    
    db = info.context["db"]
    
    # Verificar usuario
    stmt = select(Usuario).where(Usuario.id == usuario_id)
    result = await db.execute(stmt)
    if not result.scalar_one_or_none():
        return None

    # Construir query
    builder = QueryBuilder(entity=entity, limite=limite)
    for key, value in (filters or {}).items():
        if value is not None and value != "":
            builder.add_filter(key, value)
    if fields:
        builder.select_fields(fields)

    query = builder.build()

    s = SubscripcionNotificacion(
        usuario_id=usuario_id,
        nombre=nombre,
        descripcion=descripcion,
        graphql_query=query,
        campo_id="id",
        campos_comparar=fields,
        frecuencia=frecuencia,
        hora_preferida=hora_preferida,
    )
    
    db.add(s)
    await db.commit()
    await db.refresh(s)
    
    return _suscripcion_to_type(s)


async def actualizar_suscripcion(
    info,
    id: UUID,
    nombre: Optional[str] = None,
    descripcion: Optional[str] = None,
    graphql_query: Optional[str] = None,
    campo_id: Optional[str] = None,
    campos_comparar: Optional[List[str]] = None,
    frecuencia: Optional[str] = None,
    hora_preferida: Optional[int] = None,
    activo: Optional[bool] = None,
    max_errores: Optional[int] = None
) -> Optional[SuscripcionType]:
    db = info.context["db"]
    
    stmt = select(SubscripcionNotificacion).where(SubscripcionNotificacion.id == id)
    result = await db.execute(stmt)
    s = result.scalar_one_or_none()
    
    if not s:
        return None

    if nombre is not None:
        s.nombre = nombre
    if descripcion is not None:
        s.descripcion = descripcion
    if graphql_query is not None:
        s.graphql_query = graphql_query
    if campo_id is not None:
        s.campo_id = campo_id
    if campos_comparar is not None:
        s.campos_comparar = campos_comparar
    if frecuencia is not None:
        s.frecuencia = frecuencia
    if hora_preferida is not None:
        s.hora_preferida = hora_preferida
    if max_errores is not None:
        s.max_errores = max_errores
    if activo is not None:
        s.activo = activo
        if activo:
            s.pausado_por_errores = False
            s.errores_consecutivos = 0

    await db.commit()
    await db.refresh(s)
    
    return _suscripcion_to_type(s)


async def eliminar_suscripcion(
    info,
    id: UUID
) -> bool:
    db = info.context["db"]
    
    stmt = select(SubscripcionNotificacion).where(SubscripcionNotificacion.id == id)
    result = await db.execute(stmt)
    s = result.scalar_one_or_none()
    
    if not s:
        return False
    
    await db.delete(s)
    await db.commit()
    
    return True


async def ejecutar_suscripcion(
    info,
    id: UUID
) -> Optional[EjecucionType]:
    from telegram_notifications.monitor import process_subscription
    
    db = info.context["db"]
    
    stmt = select(SubscripcionNotificacion).where(SubscripcionNotificacion.id == id)
    result = await db.execute(stmt)
    s = result.scalar_one_or_none()
    
    if not s:
        return None

    # Esto debería ser async también, pero el monitor es síncrono
    process_subscription(db, s)

    # Obtener ultima ejecucion
    stmt_ejec = select(EjecucionNotificacion).where(
        EjecucionNotificacion.subscripcion_id == id
    ).order_by(EjecucionNotificacion.id.desc()).limit(1)
    
    result = await db.execute(stmt_ejec)
    e = result.scalar_one_or_none()
    
    return _ejecucion_to_type(e) if e else None


async def reactivar_suscripcion(
    info,
    id: UUID
) -> Optional[SuscripcionType]:
    db = info.context["db"]
    
    stmt = select(SubscripcionNotificacion).where(SubscripcionNotificacion.id == id)
    result = await db.execute(stmt)
    s = result.scalar_one_or_none()
    
    if not s:
        return None

    s.activo = True
    s.pausado_por_errores = False
    s.errores_consecutivos = 0
    s.ultimo_error = None

    await db.commit()
    await db.refresh(s)
    
    return _suscripcion_to_type(s)