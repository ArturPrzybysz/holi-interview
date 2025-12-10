from pydantic import BaseModel, Field

from typing import Optional, Union
from enum import Enum

# TODO: dynamic generation based on the input data schema
# We could enforce only valid columns/operators here to catch errors early.


class SortOrder(Enum):
    ASC = "asc"
    DESC = "desc"
    NONE = "none"


class FilterOperator(Enum):
    EQ = "=="
    GT = ">"
    LT = "<"
    GTE = ">="
    LTE = "<="
    NEQ = "!="


class FilterCondition(BaseModel):
    column: str = Field(
        ...,
        description="The name of the column to filter on (e.g., 'battery_health_percent')",
    )
    operator: FilterOperator = Field(..., description="The comparison operator")
    value: Union[float, int, str] = Field(
        ..., description="The value to compare against"
    )


class QueryIntent(BaseModel):
    """
    The structured intent extracted from the natural language query.
    """

    # Thinking step, optional. Might be useful for debugging or explainability.
    query_plan: str = Field(..., description="A brief description of the query plan")

    # Query definition
    filters: list[FilterCondition] = Field(
        default_factory=list, description="List of filters to apply (AND logic)"
    )
    sort_by: Optional[str] = Field(None, description="Column to sort results by")
    sort_order: SortOrder = Field(SortOrder.DESC, description="Direction of sort")
    limit: Optional[int] = Field(None, description="Max number of records to return")
