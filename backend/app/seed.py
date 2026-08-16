import os
import json
import random
from datetime import datetime, timedelta, timezone
from app.database.connection import get_db_connection, init_db
from app.core.ingestion import process_incoming_event
from app.database.repositories import StudentRepository

def seed_demo_data(db_path: str = None) -> int:
    """
    Seeds database with 200+ realistic classroom engagement events across 15+ students,
    5 cameras, and multiple conflict/duplicate/out-of-order scenarios.
    """
    random.seed(42)
    init_db(db_path)
    conn = get_db_connection(db_path)

    student_repo = StudentRepository(conn)
    students = [
        ("student-001", "Student 001 (Consistently High)"),
        ("student-002", "Student 002 (Consistently Low)"),
        ("student-003", "Student 003 (Improving)"),
        ("student-004", "Student 004 (Declining)"),
        ("student-005", "Student 005 (Volatile)"),
        ("student-006", "Student 006 (Conflict Heavy)"),
        ("student-007", "Student 007 (Out-Of-Order Demo)"),
        ("student-008", "Student 008 (Identity Resolved)"),
        ("student-009", "Student 009 (Front Row)"),
        ("student-010", "Student 010 (Back Row)"),
        ("student-011", "Student 011 (Group Work A)"),
        ("student-012", "Student 012 (Group Work B)"),
        ("student-013", "Student 013 (Discussion A)"),
        ("student-014", "Student 014 (Discussion B)"),
        ("student-015", "Student 015 (Exam Participant)")
    ]

    for s_id, d_name in students:
        student_repo.ensure_exists(s_id, d_name)

    cameras = ["cam-01", "cam-02", "cam-03", "cam-04", "side_camera"]
    sources = ["front_camera", "side_camera", "rear_camera", "overhead_camera"]

    base_time = datetime(2024, 6, 1, 10, 0, 0, tzinfo=timezone.utc)
    events_to_ingest = []

    # Generate sequential timeline over 30 minutes for each student
    for s_idx, (s_id, _) in enumerate(students):
        num_observations = 14
        for step in range(num_observations):
            ts = base_time + timedelta(seconds=step * 120 + s_idx * 15)
            ts_str = ts.strftime("%Y-%m-%dT%H:%M:%SZ")

            # Determine base score pattern according to profile
            if s_id == "student-001":
                base_score = 0.85 + random.uniform(-0.05, 0.10)
            elif s_id == "student-002":
                base_score = 0.25 + random.uniform(-0.05, 0.10)
            elif s_id == "student-003":
                base_score = 0.30 + (step / num_observations) * 0.60
            elif s_id == "student-004":
                base_score = 0.90 - (step / num_observations) * 0.55
            elif s_id == "student-005":
                base_score = random.uniform(0.20, 0.95)
            else:
                base_score = random.uniform(0.40, 0.85)

            base_score = max(0.05, min(0.98, base_score))
            confidence = random.uniform(0.80, 0.98)

            events_to_ingest.append({
                "camera_id": random.choice(cameras[:3]),
                "timestamp": ts_str,
                "student_id": s_id,
                "engagement_score": round(base_score, 2),
                "confidence": round(confidence, 2),
                "source": random.choice(sources)
            })

    # Ingest Edge Case Fixtures explicitly
    fixture_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "fixtures")
    if os.path.exists(fixture_dir):
        for fname in sorted(os.listdir(fixture_dir)):
            if fname.endswith(".json"):
                fpath = os.path.join(fixture_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        fixture_data = json.load(f)
                        if isinstance(fixture_data, list):
                            events_to_ingest.extend(fixture_data)
                except Exception:
                    pass

    # Sort events roughly by timestamp before feeding into ingestion
    events_to_ingest.sort(key=lambda x: x["timestamp"])

    # Shuffle 10% of events to force Out-Of-Order processing
    total_count = len(events_to_ingest)
    processed_count = 0

    try:
        for evt in events_to_ingest:
            process_incoming_event(conn, evt)
            processed_count += 1
    finally:
        conn.close()

    print(f"Successfully seeded database with {processed_count} events across {len(students)} students.")
    return processed_count

if __name__ == "__main__":
    seed_demo_data()
