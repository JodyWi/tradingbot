from dataclasses import replace

from backend.app.core.config import Settings
from backend.app.main import create_app
from backend.app.services.ai_providers import AIConfigurationError, OllamaProvider, create_ai_provider


class FakeAdmin:
    def __init__(self, healthy: bool) -> None:
        self.healthy = healthy

    def command(self, name: str):
        if not self.healthy:
            raise ConnectionError("offline")
        return {"ok": 1}


class FakeCollection:
    def __init__(self) -> None:
        self.documents = []

    def insert_one(self, document):
        self.documents.append(document)


class FakeRawDatabase:
    def __init__(self) -> None:
        self.collections = {}

    def __getitem__(self, name):
        return self.collections.setdefault(name, FakeCollection())


class FakeDatabase:
    def __init__(self, healthy: bool = True) -> None:
        self.healthy = healthy
        self.raw_database = FakeRawDatabase()

    def status(self):
        return {"required": True, "backend": "mongodb",
                "state": "healthy" if self.healthy else "unavailable", "ok": self.healthy}

    def collection(self, name):
        return self.raw_database[name]

    def raw(self):
        return self.raw_database

    def close(self):
        pass


def make_app(healthy: bool = True):
    settings = replace(Settings(), operator_token="test-token")
    return create_app(settings, database=FakeDatabase(healthy))


def test_liveness_and_required_mongodb_readiness() -> None:
    healthy = make_app().test_client()
    assert healthy.get("/api/health").status_code == 200
    assert healthy.get("/api/ready").get_json()["status"] == "ready"
    unavailable = make_app(False).test_client().get("/api/ready")
    assert unavailable.status_code == 503
    assert unavailable.get_json()["required_services"] == {"mongodb": "unavailable"}


def test_settings_mutation_requires_operator_and_appends_audit(monkeypatch) -> None:
    app = make_app()
    monkeypatch.setattr("backend.app.api.app.upsert_feesinfo_settings", lambda *args: None)
    client = app.test_client()
    payload = {"autoFetch": False, "autoFetchTime": "23:00"}
    assert client.post("/api/app/settings/savefeeinfo", json=payload).status_code == 403
    accepted = client.post("/api/app/settings/savefeeinfo", json=payload,
                           headers={"X-AutoLuno-Token": "test-token"})
    assert accepted.status_code == 200
    audit = app.config["PRIMARY_DATABASE"].collection("audit_events").documents
    assert audit[0]["event_type"] == "settings_fees_updated"
    assert audit[0]["outcome"] == "accepted"


def test_ai_provider_boundary_defaults_to_local_ollama() -> None:
    provider = create_ai_provider("ollama", url="http://127.0.0.1:11434")
    assert isinstance(provider, OllamaProvider)
    assert provider.capabilities() == frozenset({"generation", "embeddings"})
    try:
        create_ai_provider("unknown", url="http://127.0.0.1:11434")
    except AIConfigurationError:
        pass
    else:
        raise AssertionError("unknown provider must fail explicitly")
