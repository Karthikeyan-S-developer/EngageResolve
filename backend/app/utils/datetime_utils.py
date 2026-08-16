from datetime import datetime, timezone
from dateutil import parser

def parse_iso_timestamp(ts_str: str) -> datetime:
    """Parse any valid ISO 8601 timestamp string and return a timezone-aware UTC datetime."""
    if not isinstance(ts_str, str) or not ts_str.strip():
        raise ValueError("Timestamp must be a non-empty string.")
    
    dt = parser.isoparse(ts_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt

def normalize_to_iso_utc(ts_str: str) -> str:
    """Parse timestamp and return canonical ISO 8601 UTC string (YYYY-MM-DDTHH:MM:SSZ)."""
    dt = parse_iso_timestamp(ts_str)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

def get_current_iso_utc() -> str:
    """Get current UTC timestamp formatted as ISO 8601."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def calculate_time_difference_seconds(ts1_str: str, ts2_str: str) -> float:
    """Calculate absolute difference in seconds between two ISO timestamp strings."""
    dt1 = parse_iso_timestamp(ts1_str)
    dt2 = parse_iso_timestamp(ts2_str)
    return abs((dt1 - dt2).total_seconds())
