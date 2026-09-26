"""Small retention-aware JSONL event store for local deployments."""

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
from threading import Lock

from .models import Event


class EventStore:
    def __init__(self, path: str | Path, retention_seconds: int = 300) -> None:
        self.path = Path(path)
        self.retention_seconds = retention_seconds
        self._lock = Lock()

    def append(self, event: Event) -> None:
        with self._lock:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self._rewrite(self._retained() + [event.as_dict()])

    def recent(self, limit: int = 50) -> list[dict]:
        if limit < 1:
            raise ValueError("limit must be positive.")
        with self._lock:
            return self._retained()[-limit:]

    def clear(self) -> None:
        with self._lock:
            if self.path.exists():
                self.path.unlink()

    def _retained(self) -> list[dict]:
        if not self.path.exists():
            return []
        cutoff = datetime.now(timezone.utc) - timedelta(seconds=self.retention_seconds)
        retained = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            try:
                item = json.loads(line)
                created = datetime.fromisoformat(item["created_at"])
                if created >= cutoff:
                    retained.append(item)
            except (KeyError, TypeError, ValueError, json.JSONDecodeError):
                continue
        return retained

    def _rewrite(self, events: list[dict]) -> None:
        with self.path.open("w", encoding="utf-8") as handle:
            for event in events:
                handle.write(json.dumps(event, separators=(",", ":")) + "\n")
