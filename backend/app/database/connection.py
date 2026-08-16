import os
import sqlite3
from typing import Generator
from app.config import Config

def get_db_connection(db_path: str = None) -> sqlite3.Connection:
    if db_path is None:
        try:
            from flask import current_app
            if current_app and "DB_PATH" in current_app.config:
                db_path = current_app.config["DB_PATH"]
        except Exception:
            pass

    path = db_path or Config.DB_PATH
    
    # Ensure directory exists if path contains directories
    db_dir = os.path.dirname(os.path.abspath(path))
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)

    conn = sqlite3.connect(path, timeout=30.0, isolation_level=None) # autocommit mode, explicit transactions controlled manually if needed
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("PRAGMA journal_mode = WAL;") # Write-Ahead Logging for better concurrency
    return conn

def init_db(db_path: str = None) -> None:
    schema_file = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = get_db_connection(db_path)
    try:
        conn.executescript(schema_sql)
    finally:
        conn.close()
