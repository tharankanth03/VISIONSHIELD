"""Stable data contracts between sensing, perception, fusion, and event output."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class EventState(str, Enum):
    CLEAR = "clear"
    CANDIDATE = "candidate"
    CONFIRMED = "confirmed"


@dataclass(frozen=True)
class ObjectDetection:
    """A model-reported object label and calibrated confidence."""

    label: str
    confidence: float

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("Detection label cannot be empty.")
        if not 0 <= self.confidence <= 1:
            raise ValueError("Detection confidence must be between 0 and 1.")

    def as_dict(self) -> dict[str, Any]:
        return {"label": self.label, "confidence": self.confidence}


@dataclass(frozen=True)
class FrameObservation:
    timestamp: datetime
    rgb_score: float
    change_score: float = 0.0
    visibility: float = 1.0
    centroid: tuple[float, float] | None = None
    source: str = "rgb"
    detections: tuple[ObjectDetection, ...] = ()


@dataclass(frozen=True)
class ThermalObservation:
    timestamp: datetime
    thermal_score: float
    source: str = "mlx90640"


@dataclass(frozen=True)
class Evidence:
    timestamp: datetime
    rgb: float
    thermal: float
    change: float
    perimeter: float
    persistence: float
    visibility: float
    score: float
    state: EventState
    explanations: tuple[str, ...] = ()
    detected_objects: tuple[ObjectDetection, ...] = ()
    thermal_active: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "rgb": self.rgb,
            "thermal": self.thermal,
            "change": self.change,
            "perimeter": self.perimeter,
            "persistence": self.persistence,
            "visibility": self.visibility,
            "score": self.score,
            "state": self.state.value,
            "explanations": list(self.explanations),
            "detected_objects": [item.as_dict() for item in self.detected_objects],
            "thermal_active": self.thermal_active,
        }


@dataclass(frozen=True)
class Event:
    event_id: str
    created_at: datetime
    evidence: Evidence
    metadata: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "created_at": self.created_at.isoformat(),
            "evidence": self.evidence.as_dict(),
            "metadata": self.metadata,
        }
