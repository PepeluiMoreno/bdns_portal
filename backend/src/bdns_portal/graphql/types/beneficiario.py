from typing import Optional, List
from uuid import UUID
from datetime import datetime
import strawberry

from .catalogos import FormaJuridica, TipoBeneficiario
from .convocatoria import PageInfo

@strawberry.type
class Pseudonimo:
    id: UUID
    beneficiario_id: UUID
    pseudonimo: str
    pseudonimo_norm: str


@strawberry.type
class Beneficiario:
    id: UUID
    nif: Optional[str]
    nombre: str
    nombre_norm: str
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: Optional[str]
    updated_by: Optional[str]
    
    forma_juridica: Optional[FormaJuridica]
    tipo_beneficiario: Optional[TipoBeneficiario]
    pseudonimos: List[Pseudonimo]
    
    @strawberry.field
    def es_entidad_publica(self) -> bool:
        if not self.forma_juridica:
            return False
        return self.forma_juridica.tipo == "publica"
    
    @strawberry.field
    def es_persona_fisica(self) -> bool:
        if not self.forma_juridica:
            return False
        return self.forma_juridica.es_persona_fisica
    
    @strawberry.field
    def es_persona_juridica(self) -> bool:
        if not self.forma_juridica:
            return False
        return not self.forma_juridica.es_persona_fisica and self.forma_juridica.tipo != "desconocido"


@strawberry.type
class BeneficiarioEdge:
    cursor: str
    node: Beneficiario


@strawberry.type
class BeneficiarioConnection:
    edges: List[BeneficiarioEdge]
    page_info: 'PageInfo'   
    total_count: int

 