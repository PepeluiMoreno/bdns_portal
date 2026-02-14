# graphql/types/pagination.py
from typing import Generic, TypeVar, List, Optional
import strawberry
from dataclasses import dataclass

T = TypeVar("T")

@strawberry.type
class PageInfo:
    """Información de paginación según Relay Cursor Connection"""
    has_next_page: bool
    has_previous_page: bool
    start_cursor: Optional[str]
    end_cursor: Optional[str]
    total_count: int

@strawberry.type
class Edge(Generic[T]):
    """Arista para conexiones Relay"""
    cursor: str
    node: T

@strawberry.type
class Connection(Generic[T]):
    """Conexión Relay con paginación"""
    edges: List[Edge[T]]
    page_info: PageInfo
    total_count: int

# graphql/inputs/pagination.py
from enum import Enum
import strawberry

@strawberry.enum
class SortDirection(Enum):
    ASC = "asc"
    DESC = "desc"

@strawberry.input
class PaginationInput:
    """Parámetros de paginación estilo Relay"""
    first: Optional[int] = None
    after: Optional[str] = None
    last: Optional[int] = None
    before: Optional[str] = None

@strawberry.input
class DateRangeInput:
    """Rango de fechas para filtros"""
    from_date: Optional[strawberry.Date] = None
    to_date: Optional[strawberry.Date] = None
    
    def is_valid(self) -> bool:
        return self.from_date is not None or self.to_date is not None

@strawberry.input
class NumericRangeInput:
    """Rango numérico para filtros"""
    min: Optional[float] = None
    max: Optional[float] = None
    
    def is_valid(self) -> bool:
        return self.min is not None or self.max is not None