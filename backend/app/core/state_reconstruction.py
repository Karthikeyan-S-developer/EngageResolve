import sqlite3
from typing import Dict, Any, List, Tuple, Optional
from app.database.repositories import StudentStateRepository, EventRepository, AuditRepository
from app.core.conflict_resolution import resolve_conflict_between_events
from app.utils.datetime_utils import calculate_time_difference_seconds

def reconstruct_student_timeline(
    conn: sqlite3.Connection,
    student_id: str,
    newly_added_event: Dict[str, Any]
) -> Tuple[List[Dict[str, Any]], Optional[Dict[str, Any]]]:
    """
    Reconstructs the versioned state timeline for a student.
    Handles out-of-order event insertion deterministically.
    Returns: (reconstructed_states, audit_record_if_out_of_order)
    """
    state_repo = StudentStateRepository(conn)
    event_repo = EventRepository(conn)
    audit_repo = AuditRepository(conn)

    existing_latest = state_repo.get_latest_state(student_id)
    is_out_of_order = False

    if existing_latest and newly_added_event["timestamp"] < existing_latest["effective_timestamp"]:
        is_out_of_order = True

    # Get all ingested events for this student
    all_events = event_repo.get_events_for_student(student_id)

    # 1. Resolve conflicts among events with overlapping timestamps (<= 2 seconds apart)
    reconciled_events: List[Dict[str, Any]] = []
    conflict_audits: List[Dict[str, Any]] = []

    # Sort raw events initially by timestamp ASC
    sorted_raw = sorted(all_events, key=lambda x: (x["timestamp"], x["id"]))

    i = 0
    while i < len(sorted_raw):
        current_evt = sorted_raw[i]
        j = i + 1

        # Find any overlapping events within 2.0s timestamp difference
        competing_events = [current_evt]
        while j < len(sorted_raw):
            dt = calculate_time_difference_seconds(current_evt["timestamp"], sorted_raw[j]["timestamp"])
            if dt <= 2.0:
                competing_events.append(sorted_raw[j])
                j += 1
            else:
                break

        if len(competing_events) > 1:
            # Iteratively resolve conflict using rule engine
            winner = competing_events[0]
            for candidate in competing_events[1:]:
                winner, trace = resolve_conflict_between_events(winner, candidate)
                conflict_audits.append(trace)
            reconciled_events.append(winner)
        else:
            reconciled_events.append(current_evt)

        i = j if j > i + 1 else i + 1

    # 2. Sort final reconciled events strictly by timestamp ASC, id ASC
    reconciled_events.sort(key=lambda x: (x["timestamp"], x["id"]))

    # 3. Clear existing states for student and build versioned timeline
    state_repo.clear_states_for_student(student_id)

    new_states: List[Dict[str, Any]] = []
    previous_score = None

    for idx, evt in enumerate(reconciled_events, start=1):
        status = "OUT_OF_ORDER" if is_out_of_order else "RECONCILED" if len(all_events) > len(reconciled_events) else "VALIDATED"
        
        state_data = {
            "student_id": student_id,
            "version": idx,
            "event_id": evt["id"],
            "effective_timestamp": evt["timestamp"],
            "engagement_score": evt["engagement_score"],
            "confidence": evt["confidence"],
            "state_status": status
        }
        saved_state = state_repo.save_state(state_data)
        new_states.append(saved_state)

    # 4. Save any generated conflict audit traces
    for c_trace in conflict_audits:
        c_trace["final_score"] = c_trace["final_score"]
        audit_repo.create_log({
            "student_id": student_id,
            "event_id": c_trace["winning_event_id"],
            "decision_type": "CONFLICT_RESOLUTION",
            "input_events": c_trace["candidate_events"],
            "resolution_logic": c_trace,
            "selected_event_id": c_trace["winning_event_id"],
            "final_score": c_trace["final_score"],
            "previous_score": previous_score,
            "timestamp": c_trace["candidate_events"][0]["timestamp"]
        })

    # 5. Handle out-of-order audit record generation if applicable
    out_of_order_audit = None
    if is_out_of_order:
        out_of_order_audit = audit_repo.create_log({
            "student_id": student_id,
            "event_id": newly_added_event["id"],
            "decision_type": "OUT_OF_ORDER_EVENT",
            "input_events": [newly_added_event],
            "resolution_logic": {
                "message": f"Late-arriving event inserted at timestamp {newly_added_event['timestamp']}. Timeline reconstructed.",
                "previous_latest_timestamp": existing_latest["effective_timestamp"] if existing_latest else None,
                "reconstructed_versions_count": len(new_states)
            },
            "selected_event_id": newly_added_event["id"],
            "final_score": new_states[-1]["engagement_score"] if new_states else 0.0,
            "previous_score": existing_latest["engagement_score"] if existing_latest else None,
            "timestamp": newly_added_event["timestamp"]
        })

    return new_states, out_of_order_audit
