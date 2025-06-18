import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENABLE_BLOG = True  # Set to True when ready


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False

    # Prefer DATABASE_URL if set, otherwise build from Azure env vars
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}".format(
            user=os.getenv("AZURE_POSTGRES_USER", ""),
            password=os.getenv("AZURE_POSTGRES_PASSWORD", ""),
            host=os.getenv("AZURE_POSTGRES_HOST", ""),
            port=os.getenv("AZURE_POSTGRES_PORT", "5432"),
            db=os.getenv("AZURE_POSTGRES_DB", ""),
        ),
    )

    @property
    def ADMIN_USERNAME(self):
        if not hasattr(self, "_admin_username"):
            self._load_secrets()
        return self._admin_username

    @property
    def ADMIN_PASSWORD(self):
        if not hasattr(self, "_admin_password"):
            self._load_secrets()
        return self._admin_password

    def _load_secrets(self):
        """Lazy-load secrets from Azure Key Vault."""
        key_vault_name = os.getenv("AZURE_KEY_VAULT_NAME")
        if not key_vault_name:
            raise ValueError("AZURE_KEY_VAULT_NAME environment variable is not set")

        credential = DefaultAzureCredential()
        key_vault_url = f"https://{key_vault_name}.vault.azure.net"
        secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

        self._admin_username = secret_client.get_secret("admin-username").value
        self._admin_password = secret_client.get_secret("admin-password").value
