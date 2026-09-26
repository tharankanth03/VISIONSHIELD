"""Validated configuration for the evidence agent."""

from dataclasses import dataclass, field
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class FusionConfig:
    rgb_weight: float = 0.35
    thermal_weight: float = 0.30
    change_weight: float = 0.15
    perimeter_weight: float = 0.10
    persistence_weight: float = 0.10
    confirmation_threshold: float = 0.65
    clear_threshold: float = 0.35
    required_confirmations: int = 2
    thermal_activation_threshold: float = 0.5

    def __post_init__(self) -> None:
        weights = (
            self.rgb_weight,
            self.thermal_weight,
            self.change_weight,
            self.perimeter_weight,
            self.persistence_weight,
        )
        if any(not 0 <= value <= 1 for value in weights):
            raise ValueError("Fusion weights must be between 0 and 1.")
        if abs(sum(weights) - 1) > 1e-6:
            raise ValueError("Fusion weights must sum to 1.")
        if not 0 <= self.clear_threshold <= self.confirmation_threshold <= 1:
            raise ValueError("Thresholds must satisfy 0 <= clear <= confirm <= 1.")
        if self.required_confirmations < 1:
            raise ValueError("required_confirmations must be at least 1.")
        if not 0 <= self.thermal_activation_threshold <= 1:
            raise ValueError("thermal_activation_threshold must be between 0 and 1.")


@dataclass(frozen=True)
class NotificationConfig:
    """Optional Telegram notification settings; blank token means disabled."""

    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    timeout_seconds: float = 10.0

    @property
    def enabled(self) -> bool:
        return bool(self.telegram_bot_token and self.telegram_chat_id)

    def __post_init__(self) -> None:
        if self.timeout_seconds <= 0:
            raise ValueError("Notification timeout must be positive.")


@dataclass(frozen=True)
class AgentConfig:
    fusion: FusionConfig = field(default_factory=FusionConfig)
    retention_seconds: int = 300
    perimeter: tuple[tuple[float, float], ...] = ()
    notifications: NotificationConfig = field(default_factory=NotificationConfig)

    def __post_init__(self) -> None:
        if self.retention_seconds < 0:
            raise ValueError("retention_seconds cannot be negative.")
        if len(self.perimeter) not in (0,) and len(self.perimeter) < 3:
            raise ValueError("A perimeter must have at least three points.")

    @classmethod
    def from_json(cls, path: str | Path) -> "AgentConfig":
        raw: dict[str, Any] = json.loads(Path(path).read_text(encoding="utf-8"))
        fusion = FusionConfig(**raw.pop("fusion", {}))
        perimeter = tuple(tuple(point) for point in raw.pop("perimeter", []))
        notifications = NotificationConfig(**raw.pop("notifications", {}))
        return cls(fusion=fusion, perimeter=perimeter, notifications=notifications, **raw)
