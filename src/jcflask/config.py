import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///development.db"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///production.db")

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
