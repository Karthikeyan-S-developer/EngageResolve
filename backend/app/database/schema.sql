-- SQLite Schema for EngageResolve

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,
    display_name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    event_fingerprint TEXT UNIQUE NOT NULL,
    camera_id TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    received_at TEXT NOT NULL,
    student_id_raw TEXT NOT NULL,
    resolved_student_id TEXT NOT NULL,
    engagement_score REAL NOT NULL,
    confidence REAL NOT NULL,
    source TEXT NOT NULL,
    spatial_x REAL,
    spatial_y REAL,
    is_replay INTEGER DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (resolved_student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS student_states (
    id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL,
    version INTEGER NOT NULL,
    event_id TEXT NOT NULL,
    effective_timestamp TEXT NOT NULL,
    engagement_score REAL NOT NULL,
    confidence REAL NOT NULL,
    state_status TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (event_id) REFERENCES events(id),
    UNIQUE(student_id, version)
);

CREATE TABLE IF NOT EXISTS audit_logs (
    id TEXT PRIMARY KEY,
    student_id TEXT NOT NULL,
    event_id TEXT,
    decision_type TEXT NOT NULL,
    input_events TEXT, -- JSON array
    resolution_logic TEXT, -- JSON object
    selected_event_id TEXT,
    final_score REAL NOT NULL,
    previous_score REAL,
    timestamp TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS identity_matches (
    id TEXT PRIMARY KEY,
    raw_student_id TEXT NOT NULL,
    resolved_student_id TEXT NOT NULL,
    camera_id TEXT NOT NULL,
    temporal_score REAL NOT NULL,
    spatial_score REAL NOT NULL,
    combined_score REAL NOT NULL,
    decision TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (resolved_student_id) REFERENCES students(id)
);

CREATE TABLE IF NOT EXISTS replay_runs (
    id TEXT PRIMARY KEY,
    started_at TEXT NOT NULL,
    completed_at TEXT,
    event_count INTEGER NOT NULL,
    result_hash TEXT NOT NULL,
    status TEXT NOT NULL
);

-- Indexes for maximum query performance
CREATE INDEX IF NOT EXISTS idx_events_ts ON events(timestamp);
CREATE INDEX IF NOT EXISTS idx_events_student ON events(student_id_raw);
CREATE INDEX IF NOT EXISTS idx_events_resolved_student ON events(resolved_student_id);
CREATE INDEX IF NOT EXISTS idx_events_camera ON events(camera_id);
CREATE INDEX IF NOT EXISTS idx_events_fingerprint ON events(event_fingerprint);

CREATE INDEX IF NOT EXISTS idx_student_states_student_ver ON student_states(student_id, version);
CREATE INDEX IF NOT EXISTS idx_student_states_ts ON student_states(effective_timestamp);

CREATE INDEX IF NOT EXISTS idx_audit_logs_student ON audit_logs(student_id);
CREATE INDEX IF NOT EXISTS idx_audit_logs_ts ON audit_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_logs_type ON audit_logs(decision_type);
