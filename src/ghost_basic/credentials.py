"""Remember Ollama settings in a native OS credential vault, never a plaintext file."""

import json
import os

import keyring
from keyring.backend import KeyringBackend

from .ai import AISettings

SERVICE = "Ghost BASIC / Ollama Cloud"
ACCOUNT = "default"
NATIVE_BACKENDS = {
    "keyring.backends.macOS",
    "keyring.backends.Windows",
    "keyring.backends.SecretService",
    "keyring.backends.kwallet",
}


def native_backend() -> KeyringBackend:
    backend = keyring.get_keyring()
    if type(backend).__module__ == "keyring.backends.chainer":
        candidates = getattr(backend, "backends", [])
    else:
        candidates = [backend]
    for candidate in candidates:
        if type(candidate).__module__ in NATIVE_BACKENDS:
            return candidate  # type: ignore[no-any-return]
    raise RuntimeError("No native credential vault available")


class CredentialStore:
    def __init__(self, backend: KeyringBackend | None = None) -> None:
        self.backend = backend

    def vault(self) -> KeyringBackend:
        return self.backend if self.backend is not None else native_backend()

    def load(self) -> AISettings:
        settings = AISettings.from_env()
        if settings.api_key:
            settings.storage = "Environment"
            return settings
        try:
            value = self.vault().get_password(SERVICE, ACCOUNT)
            if not value or len(value) > 8192:
                return settings
            data = json.loads(value)
            if not isinstance(data, dict) or not isinstance(data.get("api_key"), str):
                return settings
            model = os.environ.get("OLLAMA_MODEL") or data.get("model", settings.model)
            if not isinstance(model, str):
                return settings
            saved = AISettings(data["api_key"], model, storage="Saved securely")
            saved.validate()
            return saved
        except Exception:
            # Vault backends can raise platform-specific exceptions; never echo their details.
            settings.storage = "Session only (vault unavailable)"
            return settings

    def save(self, settings: AISettings) -> bool:
        try:
            settings.validate()
            self.vault().set_password(
                SERVICE,
                ACCOUNT,
                json.dumps(
                    {
                        "api_key": settings.api_key,
                        "model": settings.model,
                    }
                ),
            )
            settings.storage = "Saved securely"
            return True
        except Exception:
            settings.storage = "Session only (vault unavailable)"
            return False
