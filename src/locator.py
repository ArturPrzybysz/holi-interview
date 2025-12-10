from pathlib import Path

def project_root() -> Path:
    return Path(__file__).parent.parent

def get_data_dir() -> Path:
    return project_root() / "data"