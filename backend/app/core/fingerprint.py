from typing import Tuple, Optional, Dict, Any
import sqlite3
from app.utils.hashing import generate_event_fingerprint
from app.database.repositories import EventRepository

def check_event_idempotency(conn: sqlite3.Connection, event_data: Dict[str, Any]) -> Tuple[bool, Optional[str], str]:
    """
    Computes deterministic SHA-256 fingerprint for event data and checks if it already exists.
    Returns: (is_duplicate: bool, existing_event_id: Optional[str], fingerprint: str)
    """
    fingerprint = generate_event_fingerprint(
        camera_id=event_data["camera_id"],
        timestamp=event_data["timestamp"],
        student_id=event_data["student_id"],
        engagement_score=event_data["engagement_score"],
        confidence=event_data["confidence"],
        source=event_data["source"]
    )
    
    event_repo = EventRepository(conn)
    existing = event_repo.get_by_fingerprint(fingerprint)
    if existing:
        return True, existing["id"], fingerprint
    return False, None, fingerprint
