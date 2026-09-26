"""Optional phone alert integrations.

Telegram is used because it works on phones, has a small HTTP API, and does not
add a runtime dependency. Notification failures are raised to the caller so a
deployment can log or retry them explicitly.
"""

from dataclasses import dataclass
import json
from typing import Protocol
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .models import Event


class AlertNotifier(Protocol):
    def format_event(self, event: Event) -> str:
        """Create a plain-text alert."""

    def send(self, message: str) -> None:
        """Deliver a message or raise an explicit error."""


class NullNotifier:
    def format_event(self, event: Event) -> str:
        return format_event_alert(event)

    def send(self, message: str) -> None:
        return None


def format_event_alert(event: Event) -> str:
    """Format a concise alert with object labels and both sensor states."""
    evidence = event.evidence
    objects = ", ".join(
        f"{item.label} ({item.confidence:.0%})"
        for item in evidence.detected_objects
    ) or "Unclassified object"
    thermal = "ACTIVE" if evidence.thermal_active else "not active"
    return (
        "VISIONSHIELD ALERT\n"
        f"Event: {event.event_id}\n"
        f"Detected: {objects}\n"
        f"RGB evidence: {evidence.rgb:.0%}\n"
        f"Thermal sensor: {thermal} ({evidence.thermal:.0%})\n"
        f"Fusion score: {evidence.score:.0%}\n"
        f"Time (UTC): {event.created_at.isoformat()}"
    )


@dataclass
class TelegramNotifier:
    """Send plain-text alerts to a Telegram chat using Bot API."""

    bot_token: str
    chat_id: str
    timeout_seconds: float = 10.0

    def format_event(self, event: Event) -> str:
        return format_event_alert(event)

    def send(self, message: str) -> None:
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = urlencode({"chat_id": self.chat_id, "text": message}).encode()
        request = Request(url, data=payload, method="POST")
        with urlopen(request, timeout=self.timeout_seconds) as response:
            body = json.loads(response.read().decode("utf-8"))
        if not body.get("ok"):
            raise RuntimeError(f"Telegram rejected alert: {body.get('description', 'unknown error')}")
