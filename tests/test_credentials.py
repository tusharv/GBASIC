import json

import pytest

from ghost_basic.ai import AISettings
from ghost_basic.credentials import CredentialStore
from ghost_basic.credentials import native_backend as real_native_backend


class MemoryVault:
    def __init__(self):
        self.value = None

    def get_password(self, service, user):
        return self.value

    def set_password(self, service, user, value):
        self.value = value


def test_key_and_model_survive_new_settings_instance(monkeypatch):
    monkeypatch.delenv("OLLAMA_API_KEY", raising=False)
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)
    vault = MemoryVault()
    store = CredentialStore(vault)
    settings = AISettings("test-secret", "gpt-oss:20b")
    assert store.save(settings)
    restored = CredentialStore(vault).load()
    assert restored.api_key == "test-secret"
    assert restored.model == "gpt-oss:20b"
    assert restored.key_status == "Not checked"
    assert restored.storage == "Saved securely"
    assert "test-secret" not in repr(restored)


def test_environment_overrides_saved_key_and_model(monkeypatch):
    vault = MemoryVault()
    store = CredentialStore(vault)
    store.save(AISettings("stored", "gemma4:31b"))
    monkeypatch.setenv("OLLAMA_API_KEY", "environment")
    monkeypatch.setenv("OLLAMA_MODEL", "gpt-oss:20b")
    result = store.load()
    assert result.api_key == "environment"
    assert result.model == "gpt-oss:20b"
    assert result.storage == "Environment"


def test_failed_vault_keeps_key_in_memory_without_plaintext_fallback(monkeypatch, tmp_path):
    class Unavailable(MemoryVault):
        def set_password(self, *args):
            raise RuntimeError("private diagnostic")

        def get_password(self, *args):
            raise RuntimeError("private diagnostic")

    monkeypatch.delenv("OLLAMA_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    store = CredentialStore(Unavailable())
    settings = AISettings("test-secret")
    assert not store.save(settings)
    assert settings.api_key == "test-secret"
    assert "Session only" in settings.storage
    assert not store.load().api_key
    assert not list(tmp_path.iterdir())


@pytest.mark.parametrize(
    "value",
    ["not json", "[]", '{"api_key":123}', json.dumps({"api_key": "bad\nkey", "model": "x"})],
)
def test_corrupted_saved_values_do_not_break_startup(monkeypatch, value):
    monkeypatch.delenv("OLLAMA_API_KEY", raising=False)
    vault = MemoryVault()
    vault.value = value
    assert not CredentialStore(vault).load().api_key


def test_native_backend_rejects_plaintext_plugins(monkeypatch):
    import keyring

    from ghost_basic.credentials import NATIVE_BACKENDS

    # The test fixture patches the selector, so inspect its real implementation
    # through the function captured before fixture setup below.
    class Plaintext:
        pass

    Plaintext.__module__ = "keyrings.alt.file"
    monkeypatch.setattr(keyring, "get_keyring", lambda: Plaintext())
    with pytest.raises(RuntimeError, match="native credential vault"):
        real_native_backend()
    assert "keyrings.alt.file" not in NATIVE_BACKENDS
