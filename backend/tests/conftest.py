import os
import pytest
import tempfile
from app.main import create_app
from app.database.connection import get_db_connection, init_db

@pytest.fixture
def temp_db_path():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    init_db(path)
    yield path
    if os.path.exists(path):
        try:
            os.remove(path)
        except Exception:
            pass

@pytest.fixture
def db_conn(temp_db_path):
    conn = get_db_connection(temp_db_path)
    yield conn
    conn.close()

@pytest.fixture
def client(temp_db_path):
    app = create_app(db_path=temp_db_path)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
