"""Typed runtime configuration for the active Flask application."""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str = "development"
    mongo_uri: str = "mongodb://127.0.0.1:27017"
    mongo_database: str = "autoluno"
    mongo_timeout_seconds: float = 3.0
    operator_token: str = ""
    ai_enabled: bool = False
    ai_provider: str = "ollama"
    ollama_url: str = "http://127.0.0.1:11434"
    ollama_model: str = "qwen2.5-coder:0.5b"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            environment=os.getenv("AUTOLUNO_ENVIRONMENT", "development"),
            mongo_uri=os.getenv("MONGO_URI", "mongodb://127.0.0.1:27017").strip(),
            mongo_database=os.getenv("MONGO_NAME", "autoluno").strip(),
            mongo_timeout_seconds=float(os.getenv("AUTOLUNO_MONGO_TIMEOUT_SECONDS", "3")),
            operator_token=os.getenv("AUTOLUNO_OPERATOR_TOKEN", "").strip(),
            ai_enabled=os.getenv("AUTOLUNO_AI_ENABLED", "false").lower() in {"1", "true", "yes"},
            ai_provider=os.getenv("AUTOLUNO_AI_PROVIDER", "ollama").strip().lower(),
            ollama_url=os.getenv("OLLAMA_URL", "http://127.0.0.1:11434").rstrip("/"),
            ollama_model=os.getenv("AUTOLUNO_OLLAMA_MODEL", "qwen2.5-coder:0.5b"),
        )

    def validate(self) -> "Settings":
        if not self.mongo_uri or not self.mongo_database or self.mongo_timeout_seconds <= 0:
            raise ValueError("MongoDB URI, database, and timeout are required")
        if not self.ai_provider:
            raise ValueError("AI provider name is required")
        return self
