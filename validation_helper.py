from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class Entity(str, Enum):
    PRODUCT = "PRODUCT"
    CUSTOMER = "CUSTOMER"

class Metric(str, Enum):
    REVENUE = "REVENUE"
    ORDERS = "ORDERS"

class Aggregation(str, Enum):
    SUM = "SUM"
    COUNT = "COUNT"
    AVG = "AVG"

class SortDirection(str, Enum):
    ASC = "ASC"
    DESC = "DESC"

class QueryIntent(BaseModel):
    entity: Entity = Field(
        description="The core business entity being queried. Always required."
    )
    metric: Optional[Metric] = Field(
        default=None,
        description="The metric to calculate. Leave null if the user doesn't specify a metric."
    )
    aggregation: Optional[Aggregation] = Field(
        default=None,
        description="The math function to apply. Leave null if raw data or system default is preferred."
    )
    sort_direction: Optional[SortDirection] = Field(
        default=None,
        description="Direction to sort results. Leave null to let backend use it's default setting."
    )
    limit: Optional[int] = Field(
        default=None,
        description="Maximum number of rows to return, Only set if explicitly requested (e.g., 'Top 5')."
    )
