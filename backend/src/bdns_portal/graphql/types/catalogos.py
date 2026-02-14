from typing import Optional, List
from uuid import UUID
import strawberry


@strawberry.type
class Finalidad:
    id: UUID
    api_id: Optional[int]
    descripcion: str
    descripcion_norm: str


@strawberry.type
class Fondo:
    id: UUID
    api_id: Optional[int]
    descripcion: str
    descripcion_norm: str


@strawberry.type
class FormaJuridica:
    id: UUID
    codigo: str
    codigo_natural: str
    descripcion: str
    descripcion_norm: str
    es_persona_fisica: bool
    tipo: str


@strawberry.type
class Instrumento:
    id: UUID
    api_id: Optional[int]
    descripcion: str
    descripcion_norm: str


@strawberry.type
class Objetivo:
    id: UUID
    api_id: Optional[int]
    descripcion: str
    descripcion_norm: str


@strawberry.type
class Organo:
    id: UUID
    codigo: str
    nombre: str
    nivel1: Optional[str]
    nivel2: Optional[str]
    nivel3: Optional[str]
    tipo: str
    padre: Optional['Organo']
    hijos: List['Organo']


@strawberry.type
class Reglamento:
    id: UUID
    ambito: Optional[str]
    api_id: Optional[int]
    descripcion: str
    descripcion_norm: str
    autorizacion: Optional[int]


@strawberry.type
class Region:
    id: UUID
    api_id: Optional[int]
    descripcion: str
    descripcion_norm: str
    padre: Optional['Region']
    hijos: List['Region']


@strawberry.type
class RegimenAyuda:
    id: UUID
    descripcion: str
    descripcion_norm: str


@strawberry.type
class SectorActividad:
    id: UUID
    codigo: str
    descripcion: str
    descripcion_norm: str
    padre: Optional['SectorActividad']
    hijos: List['SectorActividad']


@strawberry.type
class SectorProducto:
    id: UUID
    api_id: Optional[int]
    descripcion: str
    descripcion_norm: str


@strawberry.type
class TipoBeneficiario:
    id: UUID
    api_id: Optional[int]
    codigo: Optional[str]
    descripcion: str
    descripcion_norm: str