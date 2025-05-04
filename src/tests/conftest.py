import os
import tempfile

import pytest
from jcflask import create_app

@pytest.fixture
def app():
    # db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        # 'DATABASE': db_path,
    })

    yield app

    # os.close(db_fd)
    # os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture
def nav_bar_contents():
    return [
    b"Jack Cooper",
    b"Home", 
    b"About",
    ] 
