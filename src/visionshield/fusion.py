"""Visibility-aware evidence fusion and event state transitions."""

from dataclasses import dataclass

from .config import FusionConfig
from .models import EventState
from .perception import clamp


@dataclass
class EventStateMachine:
    config: FusionConfig
    state: EventState = EventState.CLEAR
    consecutive_confirmations: int = 0

    def transition(self, score: float) -> EventState:
        if score >= self.config.confirmation_threshold:
            self.consecutive_confirmations += 1
            if self.consecutive_confirmations >= self.config.required_confirmations:
                self.state = EventState.CONFIRMED
            else:
                self.state = EventState.CANDIDATE
        elif score <= self.config.clear_threshold:
            self.consecutive_confirmations = 0
            self.state = EventState.CLEAR
        else:
            self.state = EventState.CANDIDATE
        return self.state


def fuse_scores(
    *,
    rgb: float,
    thermal: float,
    change: float,
    perimeter: float,
    persistence: float,
    visibility: float,
    config: FusionConfig,
) -> tuple[float, tuple[str, ...]]:
    """Fuse calibrated signals; RGB is down-weighted when visibility is poor."""
    values = {
        "rgb": clamp(rgb),
        "thermal": clamp(thermal),
        "change": clamp(change),
        "perimeter": clamp(perimeter),
        "persistence": clamp(persistence),
    }
    visibility = clamp(visibility)
    adjusted_rgb = values["rgb"] * visibility
    score = (
        config.rgb_weight * adjusted_rgb
        + config.thermal_weight * values["thermal"]
        + config.change_weight * values["change"]
        + config.perimeter_weight * values["perimeter"]
        + config.persistence_weight * values["persistence"]
    )
    explanations = []
    if visibility < 0.5:
        explanations.append("RGB evidence reduced because visibility is below 0.5.")
    if values["perimeter"] == 0:
        explanations.append("Centroid is outside the configured perimeter or no perimeter is configured.")
    if values["persistence"] < 0.5:
        explanations.append("Evidence has not yet persisted across enough observations.")
    return clamp(score), tuple(explanations)
