from typing import Optional, List
from uuid import UUID
import strawberry
from sqlalchemy import select, and_, or_, func, desc, asc
from sqlalchemy.orm import selectinload, joinedload
import base64
import json

from bdns_core.db.models import Convocatoria, Instrumento, Region
from ..types import Convocatoria, ConvocatoriaConnection, ConvocatoriaEdge, PageInfo
from ..inputs import ConvocatoriaFilterInput, ConvocatoriaSortInput, PaginationInput


def cursor_to_offset(cursor: Optional[str]) -> int:
    if not cursor:
        return 0
    try:
        decoded = base64.b64decode(cursor).decode()
        return int(decoded.split(':')[1])
    except:
        return 0


def offset_to_cursor(offset: int, id: UUID) -> str:
    return base64.b64encode(f"convocatoria:{offset}:{id}".encode()).decode()


def build_filters(filters: Optional[ConvocatoriaFilterInput]):
    conditions = []
    if not filters:
        return conditions
    
    if filters.search:
        term = f"%{filters.search}%"
        conditions.append(
            or_(
                Convocatoria.titulo.ilike(term),
                Convocatoria.codigo_bdns.ilike(term),
                Convocatoria.descripcion.ilike(term)
            )
        )
    
    if filters.ids:
        conditions.append(Convocatoria.id.in_(filters.ids))
    
    if filters.codigo_bdns:
        conditions.append(Convocatoria.codigo_bdns == filters.codigo_bdns)
    
    if filters.titulo_contains:
        conditions.append(Convocatoria.titulo.ilike(f"%{filters.titulo_contains}%"))
    
    if filters.abierto is not None:
        conditions.append(Convocatoria.abierto == filters.abierto)
    
    if filters.mrr is not None:
        conditions.append(Convocatoria.mrr == filters.mrr)
    
    if filters.fecha_recepcion:
        if filters.fecha_recepcion.from_date:
            conditions.append(Convocatoria.fecha_recepcion >= filters.fecha_recepcion.from_date)
        if filters.fecha_recepcion.to_date:
            conditions.append(Convocatoria.fecha_recepcion <= filters.fecha_recepcion.to_date)
    
    if filters.fecha_fin_solicitud:
        if filters.fecha_fin_solicitud.from_date:
            conditions.append(Convocatoria.fecha_fin_solicitud >= filters.fecha_fin_solicitud.from_date)
        if filters.fecha_fin_solicitud.to_date:
            conditions.append(Convocatoria.fecha_fin_solicitud <= filters.fecha_fin_solicitud.to_date)
    
    if filters.presupuesto_total:
        if filters.presupuesto_total.min:
            conditions.append(Convocatoria.presupuesto_total >= filters.presupuesto_total.min)
        if filters.presupuesto_total.max:
            conditions.append(Convocatoria.presupuesto_total <= filters.presupuesto_total.max)
    
    if filters.organo_ids:
        conditions.append(Convocatoria.organo_id.in_(filters.organo_ids))
    
    if filters.finalidad_ids:
        conditions.append(Convocatoria.finalidad_id.in_(filters.finalidad_ids))
    
    if filters.instrumento_ids:
        conditions.append(
            Convocatoria.instrumentos.any(Instrumento.id.in_(filters.instrumento_ids))
        )
    
    if filters.region_ids:
        conditions.append(
            Convocatoria.regiones.any(Region.id.in_(filters.region_ids))
        )
    
    return conditions


def apply_sorting(query, sort: Optional[List[ConvocatoriaSortInput]]):
    if not sort:
        return query.order_by(desc(Convocatoria.fecha_recepcion))
    
    for s in sort:
        col = getattr(Convocatoria, s.field, None)
        if col:
            if s.direction == "asc":
                query = query.order_by(asc(col))
            else:
                query = query.order_by(desc(col))
    return query


async def get_convocatorias(
    info,
    pagination: Optional[PaginationInput] = None,
    filters: Optional[ConvocatoriaFilterInput] = None,
    sort: Optional[List[ConvocatoriaSortInput]] = None
) -> ConvocatoriaConnection:
    db = info.context["db"]
    
    query = select(Convocatoria).options(
        joinedload(Convocatoria.organo),
        joinedload(Convocatoria.reglamento),
        joinedload(Convocatoria.finalidad),
        selectinload(Convocatoria.instrumentos),
        selectinload(Convocatoria.tipos_beneficiarios),
        selectinload(Convocatoria.sectores_actividad),
        selectinload(Convocatoria.regiones),
        selectinload(Convocatoria.fondos),
        selectinload(Convocatoria.objetivos),
        selectinload(Convocatoria.documentos),
        selectinload(Convocatoria.anuncios)
    )
    
    conditions = build_filters(filters)
    if conditions:
        query = query.where(and_(*conditions))
    
    count_query = select(func.count()).select_from(Convocatoria)
    if conditions:
        count_query = count_query.where(and_(*conditions))
    total_count = await db.scalar(count_query)
    
    limit = None
    offset = 0
    
    if pagination:
        if pagination.first:
            limit = pagination.first
            if pagination.after:
                offset = cursor_to_offset(pagination.after) + 1
        elif pagination.last:
            limit = pagination.last
            if pagination.before:
                offset = max(0, cursor_to_offset(pagination.before) - pagination.last)
        elif pagination.limit:
            limit = pagination.limit
            offset = pagination.offset or 0
    
    query = apply_sorting(query, sort)
    
    if limit:
        query = query.limit(limit + 1)
    if offset:
        query = query.offset(offset)
    
    result = await db.execute(query)
    convocatorias = result.unique().scalars().all()
    
    has_next = False
    if limit and len(convocatorias) > limit:
        has_next = True
        convocatorias = convocatorias[:limit]
    
    edges = []
    for idx, c in enumerate(convocatorias):
        cursor = offset_to_cursor(offset + idx, c.id)
        edges.append(ConvocatoriaEdge(cursor=cursor, node=c))
    
    page_info = PageInfo(
        has_next_page=has_next,
        has_previous_page=offset > 0,
        start_cursor=edges[0].cursor if edges else None,
        end_cursor=edges[-1].cursor if edges else None,
        total_count=total_count
    )
    
    return ConvocatoriaConnection(edges=edges, page_info=page_info, total_count=total_count)


async def get_convocatoria_by_id(info, id: UUID) -> Optional[Convocatoria]:
    db = info.context["db"]
    query = select(Convocatoria).where(Convocatoria.id == id).options(
        joinedload(Convocatoria.organo),
        joinedload(Convocatoria.reglamento),
        joinedload(Convocatoria.finalidad),
        selectinload(Convocatoria.instrumentos),
        selectinload(Convocatoria.tipos_beneficiarios),
        selectinload(Convocatoria.sectores_actividad),
        selectinload(Convocatoria.regiones),
        selectinload(Convocatoria.fondos),
        selectinload(Convocatoria.objetivos),
        selectinload(Convocatoria.documentos),
        selectinload(Convocatoria.anuncios)
    )
    result = await db.execute(query)
    return result.scalar_one_or_none()


async def buscar_convocatorias(info, query: str, limit: int = 10) -> List[Convocatoria]:
    db = info.context["db"]
    term = f"%{query}%"
    stmt = select(Convocatoria).where(
        or_(
            Convocatoria.titulo.ilike(term),
            Convocatoria.codigo_bdns.ilike(term)
        )
    ).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())