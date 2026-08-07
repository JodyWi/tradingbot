from pathlib import Path


def test_setup_and_startup_never_install_or_start_infrastructure() -> None:
    root = Path(__file__).parents[2]
    setup = (root / "setup.sh").read_text(encoding="utf-8")
    startup = (root / "startup.sh").read_text(encoding="utf-8")
    for source in (setup, startup):
        assert "sudo " not in source
        assert "apt-get" not in source
        assert "ollama pull" not in source
    assert "START_NODE" in startup and "quarantined" in startup
