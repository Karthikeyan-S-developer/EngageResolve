import math
import sqlite3
from typing import Dict, Any, Tuple, Optional
from app.config import Config
from app.utils.datetime_utils import calculate_time_difference_seconds
from app.database.repositories import IdentityRepository, StudentRepository, EventRepository

def resolve_student_identity(
    conn: sqlite3.Connection,
    raw_student_id: str,
    camera_id: str,
    timestamp: str,
    spatial_x: Optional[float] = None,
    spatial_y: Optional[float] = None
) -> Tuple[str, Dict[str, Any]]:
    """
    Deterministically resolves raw_student_id to a canonical student_id using spatio-temporal scoring.
    Returns: (canonical_student_id: str, match_details: dict)
    """
    id_repo = IdentityRepository(conn)
    student_repo = StudentRepository(conn)
    
    # 1. Check direct mapping history
    existing_resolved_id = id_repo.find_mapping_for_raw_id(raw_student_id)
    if existing_resolved_id:
        student_repo.ensure_exists(existing_resolved_id)
        match_info = {
            "raw_student_id": raw_student_id,
            "resolved_student_id": existing_resolved_id,
            "camera_id": camera_id,
            "temporal_score": 1.0,
            "spatial_score": 1.0,
            "combined_score": 1.0,
            "decision": "EXISTING_MAPPING"
        }
        return existing_resolved_id, match_info

    # 2. Check all active students for spatio-temporal match
    cursor = conn.execute(
        """
        SELECT resolved_student_id, camera_id, timestamp, spatial_x, spatial_y
        FROM events
        ORDER BY timestamp DESC, id DESC;
        """
    )
    all_recent_events = cursor.fetchall()

    best_match_student_id: Optional[str] = None
    best_combined_score = 0.0
    best_temporal_score = 0.0
    best_spatial_score = 0.0

    time_window = Config.IDENTITY_TIME_WINDOW_SECONDS
    max_dist = Config.SPATIAL_MAX_DISTANCE
    match_threshold = Config.IDENTITY_MATCH_THRESHOLD

    seen_students = set()
    for row in all_recent_events:
        candidate_student_id = row["resolved_student_id"]
        if candidate_student_id in seen_students:
            continue
        seen_students.add(candidate_student_id)

        dt_sec = calculate_time_difference_seconds(timestamp, row["timestamp"])
        if dt_sec > time_window:
            continue

        temporal_score = 1.0 - min(dt_sec / time_window, 1.0)

        # Compute spatial score if coordinates exist on both
        if (spatial_x is not None and spatial_y is not None and 
            row["spatial_x"] is not None and row["spatial_y"] is not None):
            dist = math.sqrt((spatial_x - row["spatial_x"])**2 + (spatial_y - row["spatial_y"])**2)
            spatial_score = 1.0 - min(dist / max_dist, 1.0)
        else:
            spatial_score = 1.0 # Default fallback if spatial data missing

        combined_score = (0.6 * temporal_score) + (0.4 * spatial_score)

        if combined_score > best_combined_score:
            best_combined_score = combined_score
            best_temporal_score = temporal_score
            best_spatial_score = spatial_score
            best_match_student_id = candidate_student_id

    # 3. Decision threshold
    if best_match_student_id and best_combined_score >= match_threshold:
        resolved_id = best_match_student_id
        decision_label = "RESOLVED"
    else:
        resolved_id = raw_student_id
        decision_label = "NEW_STUDENT"
        best_temporal_score = 0.0
        best_spatial_score = 0.0
        best_combined_score = 0.0

    student_repo.ensure_exists(resolved_id)

    match_record = {
        "raw_student_id": raw_student_id,
        "resolved_student_id": resolved_id,
        "camera_id": camera_id,
        "temporal_score": round(best_temporal_score, 4),
        "spatial_score": round(best_spatial_score, 4),
        "combined_score": round(best_combined_score, 4),
        "decision": decision_label
    }
    id_repo.create_match(match_record)

    return resolved_id, match_record
