from typing import Optional, List
from uuid import UUID
from datetime import date
import strawberry


@strawberry.input
class DateRangeInput:
    from_date: Optional[date] = None
    to_date: Optional[date] = None


@strawberry.input
class NumericRangeInput:
    min: Optional[float] = None
    max: Optional[float] = None


@strawberry.input
class ConvocatoriaFilterInput:
    # Búsqueda
    search: Optional[str] = None
    ids: Optional[List[UUID]] = None
    
    # Campos
    codigo_bdns: Optional[str] = None
    titulo_contains: Optional[str] = None
    abierto: Optional[bool] = None
    mrr: Optional[bool] = None
    
    # Rangos
    fecha_recepcion: Optional[DateRangeInput] = None
    fecha_inicio_solicitud: Optional[DateRangeInput] = None
    fecha_fin_solicitud: Optional[DateRangeInput] = None
    presupuesto_total: Optional[NumericRangeInput] = None
    
    # Relaciones
    organo_ids: Optional[List[UUID]] = None
    finalidad_ids: Optional[List[UUID]] = None
    reglamento_ids: Optional[List[UUID]] = None
    instrumento_ids: Optional[List[UUID]] = None
    fondo_ids: Optional[List[UUID]] = None
    objetivo_ids: Optional[List[UUID]] = None
    region_ids: Optional[List[UUID]] = None
    sector_actividad_ids: Optional[List[UUID]] = None
    tipo_beneficiario_ids: Optional[List[UUID]] = None


@strawberry.input
class ConvocatoriaSortInput:
    field: str
    direction: str = "asc"  # asc, desc


@strawberry.input
class PaginationInput:
    first: Optional[int] = None
    after: Optional[str] = None
    last: Optional[int] = None
    before: Optional[str] = None
    offset: Optional[int] = None
    limit: Optional[int] = None