"""All tests use an isolated in-memory vault, never the developer's real credentials."""

import pytest


@pytest.fixture(autouse=True)
def isolated_credential_vault(monkeypatch):
    from ghost_basic import credentials

    class TestVault:
        def __init__(self):
            self.value = None

        def get_password(self, service, account):
            return self.value

        def set_password(self, service, account, value):
            self.value = value

    vault = TestVault()
    monkeypatch.setattr(credentials, "native_backend", lambda: vault)
    monkeypatch.delenv("OLLAMA_API_KEY", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
