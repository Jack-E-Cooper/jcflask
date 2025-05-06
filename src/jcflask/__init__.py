import os
import markdown
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for)
from jcflask.config import DevelopmentConfig, TestingConfig, ProductionConfig
from . import db

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load configuration based on the environment
    env = os.getenv('FLASK_ENV', 'production')
    if test_config:
        app.config.from_object(TestingConfig)
    elif env == 'development':
        app.config.from_object(DevelopmentConfig)
    elif env == 'production':
        app.config.from_object(ProductionConfig)
    else:
        raise ValueError(f"Unknown FLASK_ENV: {env}")

    # Initialize SQLAlchemy with the app
    db.init_app(app)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register the markdown filter
    @app.template_filter('markdown')
    def markdown_filter(content):
        return markdown.markdown(content, extensions=['fenced_code', 'codehilite'])

    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

    # Register blueprints
    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')

    from . import about
    app.register_blueprint(about.bp)

    from . import portfolio
    app.register_blueprint(portfolio.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    from . import contact
    app.register_blueprint(contact.bp)

    from . import admin
    app.register_blueprint(admin.bp)

    return app



