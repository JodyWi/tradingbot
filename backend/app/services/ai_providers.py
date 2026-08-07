"""Provider-neutral synchronous AI boundary with an Ollama adapter."""

from typing import Any, Protocol
from urllib.parse import urlparse

import requests


class AIProvider(Protocol):
    name: str
    def capabilities(self) -> frozenset[str]: ...
    def status(self) -> dict[str, Any]: ...
    def generate(self, prompt: str, *, model: str) -> str: ...


class AIConfigurationError(ValueError):
    pass


class OllamaProvider:
    name = "ollama"

    def __init__(self, url: str = "http://127.0.0.1:11434", *, session: Any = requests) -> None:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or parsed.hostname not in {
            "127.0.0.1", "localhost", "::1"
        }:
            raise AIConfigurationError("Ollama URL must use a local loopback address")
        self.url = url.rstrip("/")
        self.session = session

    def capabilities(self) -> frozenset[str]:
        return frozenset({"generation", "embeddings"})

    def status(self) -> dict[str, Any]:
        try:
            response = self.session.get(f"{self.url}/api/tags", timeout=3)
            response.raise_for_status()
            return {"provider": self.name, "state": "healthy", "ok": True,
                    "capabilities": sorted(self.capabilities())}
        except requests.RequestException as exc:
            return {"provider": self.name, "state": "unavailable", "ok": False,
                    "capabilities": sorted(self.capabilities()), "error": type(exc).__name__}

    def generate(self, prompt: str, *, model: str) -> str:
        response = self.session.post(
            f"{self.url}/api/chat",
            json={"model": model, "stream": False,
                  "messages": [{"role": "system", "content": "Return only strict JSON."},
                               {"role": "user", "content": prompt}], "format": "json"},
            timeout=10,
        )
        response.raise_for_status()
        content = response.json().get("message", {}).get("content", "")
        if not content:
            raise ValueError("empty AI provider response")
        return str(content)


def create_ai_provider(name: str, *, url: str, session: Any = requests) -> AIProvider:
    if name.strip().lower() == "ollama":
        return OllamaProvider(url, session=session)
    raise AIConfigurationError(f"Unsupported AI provider {name!r}; register an adapter explicitly")
