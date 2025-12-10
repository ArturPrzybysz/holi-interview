import pytest
import pandas as pd
from src.query_engine import QueryEngine
from src.types.query_types import (
    QueryIntent, 
    FilterCondition, 
    FilterOperator, 
    SortOrder
)

# TODO: move to tests/assets
SAMPLE_DATA = [
  {
    "vehicle_id": "CAR040TYT7D5",
    "timestamp": "2024-11-22T13:00:00Z",
    "battery_health_percent": 92.4,
    "odometer_km": 36744
  },
  {
    "vehicle_id": "VIN0466HID25",
    "timestamp": "2024-11-21T15:00:00Z",
    "battery_health_percent": 97.7,
    "odometer_km": 87392
  },
  {
    "vehicle_id": "VIN035O7UUBC",
    "timestamp": "2024-11-20T16:00:00Z",
    "battery_health_percent": 94.6,
    "odometer_km": 41831
  },
  {
    "vehicle_id": "CAR001DPBHSA",
    "timestamp": "2024-11-20T09:00:00Z",
    "battery_health_percent": 77.4,
    "odometer_km": 115326
  }
]

@pytest.fixture
def query_engine():
    """Fixture to initialize QueryEngine with sample data."""
    df = pd.DataFrame(SAMPLE_DATA)
    return QueryEngine(df)

# --- Validation Tests ---

def test_validate_query_intent_valid(query_engine):
    intent = QueryIntent(
        query_plan="Test valid",
        filters=[FilterCondition(column="battery_health_percent", operator=FilterOperator.GT, value=90)],
        sort_by="odometer_km"
    )
    assert query_engine.validate_query_intent(intent) is True

def test_validate_query_intent_invalid_filter_column(query_engine):
    intent = QueryIntent(
        query_plan="Test invalid filter",
        filters=[FilterCondition(column="non_existent_col", operator=FilterOperator.EQ, value=10)]
    )
    with pytest.raises(ValueError, match="Column 'non_existent_col' does not exist"):
        query_engine.validate_query_intent(intent)

def test_validate_query_intent_invalid_sort_column(query_engine):
    intent = QueryIntent(
        query_plan="Test invalid sort",
        sort_by="random_col"
    )
    with pytest.raises(ValueError, match="Sort column 'random_col' does not exist"):
        query_engine.validate_query_intent(intent)

# --- Filtering Tests ---

def test_execute_query_filter_eq(query_engine):
    intent = QueryIntent(
        query_plan="Filter equality",
        filters=[FilterCondition(column="vehicle_id", operator=FilterOperator.EQ, value="CAR040TYT7D5")]
    )
    result = query_engine.execute_query(intent)
    assert len(result) == 1
    assert result.iloc[0]["vehicle_id"] == "CAR040TYT7D5"

def test_execute_query_filter_gt(query_engine):
    intent = QueryIntent(
        query_plan="Filter greater than",
        filters=[FilterCondition(column="battery_health_percent", operator=FilterOperator.GT, value=95.0)]
    )
    result = query_engine.execute_query(intent)
    assert len(result) == 1
    assert result.iloc[0]["battery_health_percent"] == 97.7

def test_execute_query_filter_lte(query_engine):
    intent = QueryIntent(
        query_plan="Filter less than or equal",
        filters=[FilterCondition(column="odometer_km", operator=FilterOperator.LTE, value=41831)]
    )
    # Should match 36744 and 41831
    result = query_engine.execute_query(intent)
    assert len(result) == 2
    assert 36744 in result["odometer_km"].values
    assert 41831 in result["odometer_km"].values

def test_execute_query_filter_neq(query_engine):
    intent = QueryIntent(
        query_plan="Filter not equal",
        filters=[FilterCondition(column="vehicle_id", operator=FilterOperator.NEQ, value="CAR001DPBHSA")]
    )
    result = query_engine.execute_query(intent)
    assert len(result) == 3
    assert "CAR001DPBHSA" not in result["vehicle_id"].values

def test_execute_query_multiple_filters(query_engine):
    """Test AND logic between multiple filters."""
    intent = QueryIntent(
        query_plan="Multiple filters",
        filters=[
            FilterCondition(column="battery_health_percent", operator=FilterOperator.GT, value=90),
            FilterCondition(column="odometer_km", operator=FilterOperator.LT, value=50000)
        ]
    )
    result = query_engine.execute_query(intent)
    # Should match CAR040TYT7D5 (92.4%, 36744km) and VIN035O7UUBC (94.6%, 41831km)
    assert len(result) == 2
    assert "CAR040TYT7D5" in result["vehicle_id"].values
    assert "VIN035O7UUBC" in result["vehicle_id"].values

# --- Sorting Tests ---

def test_execute_query_sort_asc(query_engine):
    intent = QueryIntent(
        query_plan="Sort ascending",
        sort_by="battery_health_percent",
        sort_order=SortOrder.ASC
    )
    result = query_engine.execute_query(intent)
    # Lowest battery health (77.4) should be first
    assert result.iloc[0]["battery_health_percent"] == 77.4
    assert result.iloc[-1]["battery_health_percent"] == 97.7

def test_execute_query_sort_desc(query_engine):
    intent = QueryIntent(
        query_plan="Sort descending",
        sort_by="odometer_km",
        sort_order=SortOrder.DESC
    )
    result = query_engine.execute_query(intent)
    # Highest odometer (115326) should be first
    assert result.iloc[0]["odometer_km"] == 115326
    assert result.iloc[-1]["odometer_km"] == 36744

# --- Limit Tests ---

def test_execute_query_limit(query_engine):
    intent = QueryIntent(
        query_plan="Test limit",
        limit=2
    )
    result = query_engine.execute_query(intent)
    assert len(result) == 2

# --- Complex Integration Test ---

def test_execute_query_complex(query_engine):
    """Test Filter, Sort, and Limit combined."""
    intent = QueryIntent(
        query_plan="Complex query",
        # Get vehicles with good battery (>90)
        filters=[FilterCondition(column="battery_health_percent", operator=FilterOperator.GT, value=90.0)],
        # Sort by lowest mileage first
        sort_by="odometer_km",
        sort_order=SortOrder.ASC,
        # Only take top 1
        limit=1
    )
    result = query_engine.execute_query(intent)
    
    assert len(result) == 1
    assert result.iloc[0]["vehicle_id"] == "CAR040TYT7D5"