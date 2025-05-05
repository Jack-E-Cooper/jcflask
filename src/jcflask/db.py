from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import current_app, g

db = SQLAlchemy()  # Initialize SQLAlchemy instance

def get_connection():
    """Get a connection to the database."""
    if 'db_connection' not in g:
        g.db_connection = db.session.connection()
    return g.db_connection

def close_connection(exception=None):
    """Close the database session and remove it from the context."""
    db.session.remove()
    g.pop('db_connection', None)

def init_app(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    app.teardown_appcontext(close_connection)  # Ensure cleanup on app context teardown

def create_all():
    """Create all database tables."""
    with current_app.app_context():
        db.create_all()