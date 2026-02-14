from typing import Optional, List
from uuid import UUID
from datetime import date, datetime
import strawberry
import base64
import json

from .catalogos import (
    Organo, Reglamento, Finalidad, Instrumento,
    TipoBeneficiario, SectorActividad, Region,
    Fondo, Objetivo, SectorProducto
)


# ==================== PAGINACIÓN ====================
@strawberry.type
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]
    total_count: int


@strawberry.type
class ConvocatoriaEdge:
    cursor: str
    node: 'Convocatoria'


@strawberry.type
class ConvocatoriaConnection:
    edges: List[ConvocatoriaEdge]
    page_info: PageInfo
    total_count: int


# ==================== DOCUMENTOS Y ANUNCIOS ====================
@strawberry.type
class DocumentoConvocatoria:
    id: UUID
    api_id: Optional[int]
    nombre_fichero: Optional[str]
    descripcion: Optional[str]
    longitud: Optional[int]
    fecha_modificacion: Optional[date]
    fecha_publicacion: Optional[date]
    convocatoria_id: UUID


@strawberry.type
class AnuncioConvocatoria:
    id: UUID
    num_anuncio: Optional[int]
    titulo: Optional[str]
    titulo_leng: Optional[str]
    texto: Optional[str]
    texto_leng: Optional[str]
    url: Optional[str]
    cve: Optional[str]
    descripcion_diario_oficial: Optional[str]
    fecha_publicacion: Optional[date]
    convocatoria_id: UUID


# ==================== CONVOCATORIA ====================
@strawberry.type
class Convocatoria:
    id: UUID
    codigo_bdns: str
    titulo: Optional[str]
    descripcion: Optional[str]
    descripcion_leng: Optional[str]
    fecha_recepcion: Optional[date]
    fecha_inicio_solicitud: Optional[date]
    fecha_fin_solicitud: Optional[date]
    sede_electronica: Optional[str]
    url_bases_reguladoras: Optional[str]
    url_ayuda_estado: Optional[str]
    presupuesto_total: Optional[float]
    mrr: bool
    tipo_convocatoria: Optional[str]
    descripcion_bases_reguladoras: Optional[str]
    se_publica_diario_oficial: Optional[bool]
    abierto: Optional[bool]
    ayuda_estado: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: Optional[str]
    updated_by: Optional[str]
    
    # Relaciones
    organo: Optional[Organo]
    reglamento: Optional[Reglamento]
    finalidad: Optional[Finalidad]
    instrumentos: List[Instrumento]
    tipos_beneficiarios: List[TipoBeneficiario]
    sectores_actividad: List[SectorActividad]
    regiones: List[Region]
    fondos: List[Fondo]
    objetivos: List[Objetivo]
    sectores_producto: List[SectorProducto]
    documentos: List[DocumentoConvocatoria]
    anuncios: List[AnuncioConvocatoria]
    
    @strawberry.field
    def estado(self) -> str:
        hoy = date.today()
        if self.fecha_fin_solicitud and self.fecha_fin_solicitud < hoy:
            return "CERRADA"
        if self.fecha_inicio_solicitud and self.fecha_inicio_solicitud > hoy:
            return "PROXIMA"
        if self.abierto:
            return "ABIERTA"
        return "CERRADA"
    
    @strawberry.field
    def dias_restantes(self) -> Optional[int]:
        if self.fecha_fin_solicitud and self.estado == "ABIERTA":
            delta = self.fecha_fin_solicitud - date.today()
            return delta.days if delta.days >= 0 else 0
        return None
    
    @strawberry.field
    def presupuesto_formateado(self) -> Optional[str]:
        if self.presupuesto_total:
            return f"{self.presupuesto_total:,.2f}€"
        return None