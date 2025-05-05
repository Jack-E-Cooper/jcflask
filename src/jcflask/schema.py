from jcflask import db
from jcflask.models import BlogPost  # Import the BlogPost model

def initialize_database():
    """Create all tables in the database."""
    db.create_all()

if __name__ == "__main__":
    from jcflask import create_app

    # Create the app and initialize the database
    app = create_app()
    with app.app_context():
        print("Initializing the database...")
        initialize_database()
        print("Database initialized successfully.")
