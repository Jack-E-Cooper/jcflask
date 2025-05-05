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

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    DEBUG = False


# SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
# MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
# MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')