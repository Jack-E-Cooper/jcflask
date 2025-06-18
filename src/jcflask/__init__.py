import os
from flask import Flask, send_from_directory, url_for
from jcflask.config import DevelopmentConfig, TestingConfig, ProductionConfig
from . import db
import markdown


def create_app(test_config=None):
    """Create and configure the Flask application."""
    os.environ.setdefault(
        "FLASK_ENV", "development"
    )  # Default to development for local use
    app = Flask(__name__)

    # Load configuration based on the environment
    env = os.getenv("FLASK_ENV", "production")
    if test_config:
        app.config.from_object(TestingConfig)
    elif env == "development":
        app.config.from_object(DevelopmentConfig)
    elif env == "production":
        app.config.from_object(ProductionConfig)
    else:
        raise ValueError(f"Unknown FLASK_ENV: {env}")

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Register the markdown filter
    @app.template_filter("markdown")
    def markdown_filter(content):
        return markdown.markdown(content, extensions=["fenced_code", "codehilite"])

    # Create database schema in development and testing environments
    if env in ["development", "testing"]:
        with app.app_context():
            db.create_all()

    # Ensure the instance folder exists (skip in production if not needed)
    if env != "production":
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

    # Image URL handler
    def image_url(filename):
        if app.config.get("ENV") == "production":
            # Example: Use Azure Blob Storage URL
            blob_base = app.config.get("BLOB_IMAGE_BASE_URL", "https://jcflaskfilestore.blob.core.windows.net/jcflask-website-images/")
            return f"{blob_base}{filename}"
        else:
            return url_for('static', filename=f'images/{filename}')

    app.jinja_env.globals['image_url'] = image_url

    @app.route("/favicon.ico")
    def favicon():
        return send_from_directory(
            os.path.join(app.root_path, "static"),
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    # Register blueprints
    from . import home

    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint="index")

    from . import about

    app.register_blueprint(about.bp)

    from . import portfolio

    app.register_blueprint(portfolio.bp)

    from . import contact

    app.register_blueprint(contact.bp)

    from . import admin

    app.register_blueprint(admin.bp)

    from . import project

    app.register_blueprint(project.bp)

    # Register gallery blueprint
    from flask import Blueprint, render_template

    gallery_bp = Blueprint("gallery", __name__, url_prefix="/gallery")

    @gallery_bp.route("/")
    def gallery():
        return render_template("gallery.html")

    app.register_blueprint(gallery_bp)

    # Conditionally register blog
    if app.config.get("ENABLE_BLOG", False):
        from . import blog

        app.register_blueprint(blog.bp)

    return app
