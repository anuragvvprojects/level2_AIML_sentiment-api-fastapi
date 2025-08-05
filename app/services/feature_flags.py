import os

def is_enabled(flag: str, default: bool = False) -> bool:
    """Simple env-based feature flag.
    Reads FLAG_<NAME>, e.g., FLAG_EXPLAIN=true.
    """
    val = os.getenv(f"FLAG_{flag.upper()}")
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on", "y"}
