from typing import Optional, List
from uuid import UUID
import strawberry


@strawberry.input
class CatalogoFilterInput:
    search: Optional[str] = None
    ids: Optional[List[UUID]] = None
    api_ids: Optional[List[int]] = None
    descripcion_contains: Optional[str] = None
    codigo_contains: Optional[str] = None