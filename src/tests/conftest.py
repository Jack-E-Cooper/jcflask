import os
import tempfile
import pytest
from jcflask import create_app
from jcflask.db import db
from jcflask.models import BlogPost

@pytest.fixture(scope="session")
def app():
    """Session-scoped app fixture for live server tests."""
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
    })

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope="function", autouse=True)
def reset_db(app):
    """Reset the database before each test."""
    with app.app_context():
        db.session.query(BlogPost).delete()  # Clear all blog posts
        db.session.commit()

@pytest.fixture(scope="session")
def live_server(app, live_server):
    """Session-scoped live server fixture."""
    live_server._app = app  # Explicitly set the app for the live server
    live_server.port = 5001  # Specify a custom port to avoid conflicts
    live_server.start()
    return live_server

