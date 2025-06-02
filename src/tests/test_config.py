import os
import pytest
from unittest.mock import patch, MagicMock
from jcflask.config import ProductionConfig


@pytest.fixture
def mock_key_vault_env():
    """Fixture to set up the environment variable for Azure Key Vault."""
    with patch.dict(os.environ, {"AZURE_KEY_VAULT_NAME": "mock-key-vault"}):
        yield


@pytest.fixture
def mock_secret_client():
    """Fixture to mock the SecretClient and its methods."""
    with patch("jcflask.config.SecretClient") as mock_client:
        mock_instance = MagicMock()
        mock_instance.get_secret.side_effect = lambda name: MagicMock(
            value=f"mock-{name}"
        )
        mock_client.return_value = mock_instance
        yield mock_instance


def test_load_secrets_from_key_vault(mock_key_vault_env, mock_secret_client):
    """Test that secrets are correctly loaded from Azure Key Vault."""
    config = ProductionConfig()

    # Access the properties to trigger the lazy loading
    admin_username = config.ADMIN_USERNAME
    admin_password = config.ADMIN_PASSWORD

    # Assertions
    assert admin_username == "mock-admin-username"
    assert admin_password == "mock-admin-password"
    mock_secret_client.get_secret.assert_any_call("admin-username")
    mock_secret_client.get_secret.assert_any_call("admin-password")


def test_missing_key_vault_name():
    """Test that an error is raised if AZURE_KEY_VAULT_NAME is not set."""
    with patch.dict(os.environ, {}, clear=True):
        config = ProductionConfig()
        with pytest.raises(
            ValueError, match="AZURE_KEY_VAULT_NAME environment variable is not set"
        ):
            _ = config.ADMIN_USERNAME  # Access the property to trigger the error
