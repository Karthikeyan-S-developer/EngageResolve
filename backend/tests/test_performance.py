import time
from app.core.ingestion import process_incoming_event

def test_ingestion_performance_benchmark(db_conn):
    start_time = time.time()
    total_events = 150

    for i in range(total_events):
        event = {
            "camera_id": f"cam-0{(i % 4) + 1}",
            "timestamp": f"2024-06-01T10:00:{i % 60:02d}Z",
            "student_id": f"student-bench-{(i % 10) + 1:03d}",
            "engagement_score": round((i % 10) / 10.0, 2),
            "confidence": 0.90,
            "source": "front_camera"
        }
        process_incoming_event(db_conn, event)

    duration = time.time() - start_time
    events_per_sec = total_events / duration if duration > 0 else total_events

    print(f"\n[BENCHMARK] Processed {total_events} events in {duration:.3f}s ({events_per_sec:.1f} events/sec)")
    assert events_per_sec >= 20.0 # Standard safety bar for local dev machines
