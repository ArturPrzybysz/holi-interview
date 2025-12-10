from src.types.query_types import QueryIntent, FilterCondition, FilterOperator, SortOrder

user_query = """Find me the top 5 vehicles with over 50,000 km on the odometer, that have a battery health below 90%.
Sort them so the vehicles with the lowest battery health appear first."""

example_intent = QueryIntent(
    query_plan="Filter for odometer > 50k and battery < 90%, then sort by battery ascending to show worst health first, limiting to top 5.",
    filters=[
        FilterCondition(
            column="odometer_km", operator=FilterOperator.GT, value=50000
        ),
        FilterCondition(
            column="battery_health_percent", operator=FilterOperator.LT, value=90
        ),
    ],
    sort_by="battery_health_percent",
    sort_order=SortOrder.ASC,
    limit=5,
)



example_str = f"Example user input:\n{user_query}\n\nExpected output:\n{example_intent.model_dump_json()}"