import os
import tempfile
from app.database.connection import get_db_connection
from app.seed import seed_demo_data
from app.database.repositories import StudentStateRepository, AuditRepository
from app.utils.hashing import calculate_state_result_hash

def test_system_wide_determinism(temp_db_path):
    # Seed db 1
    seed_demo_data(temp_db_path)
    conn1 = get_db_connection(temp_db_path)
    states1 = StudentStateRepository(conn1).list_all_latest_states()
    audits1 = AuditRepository(conn1).list_all(limit=10000)
    hash1 = calculate_state_result_hash(states1, audits1)
    conn1.close()

    # Replay/reseed in isolated DB 2 (temp file)
    fd2, path2 = tempfile.mkstemp(suffix=".db")
    os.close(fd2)
    try:
        seed_demo_data(path2)
        conn2 = get_db_connection(path2)
        states2 = StudentStateRepository(conn2).list_all_latest_states()
        audits2 = AuditRepository(conn2).list_all(limit=10000)
        hash2 = calculate_state_result_hash(states2, audits2)
        conn2.close()

        # Assert 100% state hash equality
        assert hash1 == hash2
    finally:
        if os.path.exists(path2):
            try:
                os.remove(path2)
            except Exception:
                pass
