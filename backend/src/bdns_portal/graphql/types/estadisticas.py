# graphql/types/estadisticas.py
from typing import Optional, List
from uuid import UUID
from datetime import date
import strawberry


@strawberry.type
class EstadisticasConcesiones:
    # Dimensiones
    tipo_entidad: Optional[str] = None
    organo_id: Optional[str] = None
    organo_nombre: Optional[str] = None
    beneficiario_id: Optional[str] = None
    beneficiario_nombre: Optional[str] = None
    region_id: Optional[str] = None
    region_nombre: Optional[str] = None
    regimen: Optional[str] = None
    
    # Métricas
    anio: Optional[int] = None
    numero_concesiones: int = 0
    importe_total: float = 0
    importe_medio: Optional[float] = None
    
    # Beneficiarios recurrentes
    primera_concesion: Optional[date] = None
    ultima_concesion: Optional[date] = None


@strawberry.type
class EvolucionMensual:
    mes: int
    numero_concesiones: int
    importe_mensual: float
    acumulado_anual: float
    porcentaje_total: float


@strawberry.type
class EstadisticasRegimen:
    regimen: str
    anio: Optional[int]
    numero_concesiones: int
    importe_total: float
    porcentaje_importe: float
    porcentaje_concesiones: float


@strawberry.type
class EstadisticasRegion:
    region_id: str
    region_nombre: str
    anio: Optional[int]
    numero_concesiones: int
    importe_total: float
    numero_beneficiarios: int
    importe_medio: float


@strawberry.type
class TopConvocatoria:
    convocatoria_id: str
    codigo_bdns: str
    titulo: Optional[str]
    anio: Optional[int]
    importe_concedido: float
    presupuesto_total: Optional[float]
    porcentaje_ejecutado: float
    numero_beneficiarios: int


@strawberry.type
class ComparativaAnual:
    anio_base: int
    anio_comparar: int
    
    # Importe
    total_concedido_base: float
    total_concedido_comparar: float
    variacion_importe: float
    variacion_importe_porcentual: float
    
    # Concesiones
    numero_concesiones_base: int
    numero_concesiones_comparar: int
    variacion_concesiones: int
    variacion_concesiones_porcentual: float
    
    # Importe medio
    importe_medio_base: float
    importe_medio_comparar: float
    variacion_importe_medio: float
    variacion_importe_medio_porcentual: float
    
    # Beneficiarios
    numero_beneficiarios_base: int
    numero_beneficiarios_comparar: int
    variacion_beneficiarios: int
    variacion_beneficiarios_porcentual: float


@strawberry.input
class FiltroEstadisticas:
    anio: Optional[int] = None
    anio_desde: Optional[int] = None
    anio_hasta: Optional[int] = None
    tipo_entidad: Optional[str] = None
    organo_id: Optional[UUID] = None
    region_id: Optional[UUID] = None
    regimen: Optional[str] = None
