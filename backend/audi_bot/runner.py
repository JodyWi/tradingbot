from __future__ import annotations

import threading
from dataclasses import dataclass, field

from autoluno.backend.audi_bot.decision import run_decision_cycle
from autoluno.backend.audi_bot.utils import get_bot_settings


@dataclass
class AudiBotController:
    _thread: threading.Thread | None = None
    _stop_event: threading.Event = field(default_factory=threading.Event)
    _lock: threading.Lock = field(default_factory=threading.Lock)
    _active_pair: str | None = None

    def start(self, pair: str | None = None) -> dict:
        settings = get_bot_settings()
        if not settings.get("strategyEnabled", False):
            return {"status": "disabled", "message": "Audi Bot strategy is disabled by settings."}
        with self._lock:
            if self._thread and self._thread.is_alive():
                return {"status": "running", "message": "Audi Bot strategy is already running."}
            self._stop_event.clear()
            self._active_pair = pair or "XBTZAR"
            self._thread = threading.Thread(target=self._loop, daemon=True)
            self._thread.start()
        return {"status": "running", "message": "Audi Bot strategy started."}

    def stop(self) -> dict:
        with self._lock:
            self._stop_event.set()
            self._active_pair = None
        return {"status": "stopped", "message": "Audi Bot strategy stopped."}

    def step(self, pair: str) -> dict:
        return run_decision_cycle(pair=pair)

    def _loop(self) -> None:
        settings = get_bot_settings()
        interval_seconds = max(60, int(settings["strategyIntervalMinutes"]) * 60)
        pair = self._active_pair or "XBTZAR"
        while not self._stop_event.is_set():
            run_decision_cycle(pair=pair)
            self._stop_event.wait(interval_seconds)


controller = AudiBotController()


def start(pair: str | None = None):
    return controller.start(pair=pair)


def stop():
    return controller.stop()


def step(pair: str):
    return controller.step(pair)
