import pandas as pd

from src.types.query_types import FilterOperator, QueryIntent, SortOrder


class QueryEngine:
    data: pd.DataFrame

    def __init__(self, data: pd.DataFrame):
        self.data = data

    def validate_query_intent(self, query_intent: QueryIntent) -> bool:
        # Basic validation to ensure columns exist in the DataFrame
        # Would be not necessary with dynamic generation of QueryIntent based on schema
        for condition in query_intent.filters:
            if condition.column not in self.data.columns:
                raise ValueError(
                    f"Column '{condition.column}' does not exist in the data."
                )
        if query_intent.sort_by and query_intent.sort_by not in self.data.columns:
            raise ValueError(
                f"Sort column '{query_intent.sort_by}' does not exist in the data."
            )
        return True

    def execute_query(self, query_intent: QueryIntent) -> pd.DataFrame:
        df = self.data.copy()

        # Apply filters
        for condition in query_intent.filters:
            if condition.operator == FilterOperator.EQ:
                df = df[df[condition.column] == condition.value]
            elif condition.operator == FilterOperator.GT:
                df = df[df[condition.column] > condition.value]
            elif condition.operator == FilterOperator.LT:
                df = df[df[condition.column] < condition.value]
            elif condition.operator == FilterOperator.GTE:
                df = df[df[condition.column] >= condition.value]
            elif condition.operator == FilterOperator.LTE:
                df = df[df[condition.column] <= condition.value]
            elif condition.operator == FilterOperator.NEQ:
                df = df[df[condition.column] != condition.value]

        # Apply sorting
        if query_intent.sort_by:
            ascending = query_intent.sort_order == SortOrder.ASC
            df = df.sort_values(by=query_intent.sort_by, ascending=ascending)

        # Apply limit
        if query_intent.limit is not None:
            df = df.head(query_intent.limit)

        return df.reset_index(drop=True)
