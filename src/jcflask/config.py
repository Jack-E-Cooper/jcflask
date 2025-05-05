class Config:
    # General Flask Config
    SECRET_KEY = 'your_secret_key'  # Replace with a secure key
    DEBUG = False
    TESTING = False

    # Mail Configuration
    MAIL_SERVER = 'smtp.example.com'  # Replace with your SMTP server
    MAIL_PORT = 587  # Replace with your SMTP port
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'your_email@example.com'  # Replace with your email
    MAIL_PASSWORD = 'your_password'  # Replace with your email password
    MAIL_DEFAULT_SENDER = 'noreply@example.com'  # Replace with a no-reply email

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = 'sqlite:///jcflask.db'  # Default to SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'  # Development database

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'  # Testing database

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///production.db'  # Production database