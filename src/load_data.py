import pandas as pd
from pathlib import Path
from src.types.input_types import VehicleTelemetry
import json

def load_data(file_path: Path) -> pd.DataFrame:
    raw_data = json.load(file_path.open("r"))
    df = pd.DataFrame(raw_data)
    # validate using pydantic
    for record in df.to_dict(orient="records"):
        VehicleTelemetry(**record)
    return df
