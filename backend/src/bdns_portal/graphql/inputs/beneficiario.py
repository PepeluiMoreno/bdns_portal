from typing import Optional, List
from uuid import UUID
import strawberry


@strawberry.input
class BeneficiarioFilterInput:
    search: Optional[str] = None
    ids: Optional[List[UUID]] = None
    nif: Optional[str] = None
    nombre_contains: Optional[str] = None
    forma_juridica_ids: Optional[List[UUID]] = None
    tipo_beneficiario_ids: Optional[List[UUID]] = None
    es_entidad_publica: Optional[bool] = None
    es_persona_fisica: Optional[bool] = None
    es_persona_juridica: Optional[bool] = None


@strawberry.input
class BeneficiarioSortInput:
    field: str
    direction: str = "asc"