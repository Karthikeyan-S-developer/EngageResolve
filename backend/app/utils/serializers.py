import json
import sqlite3
from typing import Dict, Any, Union

def row_to_dict(row: Union[sqlite3.Row, Dict[str, Any]]) -> Dict[str, Any]:
    """Convert an sqlite3.Row object to a standard Python dictionary."""
    if row is None:
        return None
    if isinstance(row, dict):
        return row
    d = dict(row)
    # Parse JSON fields if present
    for json_field in ("input_events", "resolution_logic"):
        if json_field in d and isinstance(d[json_field], str):
            try:
                d[json_field] = json.loads(d[json_field])
            except Exception:
                pass
    return d

def format_api_success(data: Any, status_code: int = 200) -> tuple:
    """Format standard API success response."""
    return {"success": True, "data": data}, status_code

def format_api_error(code: str, message: str, status_code: int = 400) -> tuple:
    """Format standard API error response."""
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message
        }
    }, status_code
