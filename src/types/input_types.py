from pydantic import BaseModel


class VehicleTelemetry(BaseModel):
    vehicle_id: str
    timestamp: str
    battery_health_percent: float
    odometer_km: int
