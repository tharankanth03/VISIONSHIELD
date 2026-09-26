"""Deterministic perception helpers and extension protocols for model adapters."""

from math import hypot
from typing import Protocol, Sequence

from .models import FrameObservation, ThermalObservation


class RGBDetector(Protocol):
    def score(self, frame: FrameObservation) -> float:
        """Return a calibrated target score in the inclusive range [0, 1]."""


class ThermalModel(Protocol):
    def score(self, frame: ThermalObservation) -> float:
        """Return a calibrated thermal activity score in the inclusive range [0, 1]."""


def clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def point_in_polygon(
    point: tuple[float, float], polygon: Sequence[tuple[float, float]]
) -> bool:
    """Return whether a point is inside a polygon using ray casting."""
    if len(polygon) < 3:
        return False
    x, y = point
    inside = False
    previous = polygon[-1]
    for current in polygon:
        x1, y1 = current
        x2, y2 = previous
        intersects = (y1 > y) != (y2 > y)
        if intersects:
            crossing_x = (x2 - x1) * (y - y1) / ((y2 - y1) or 1e-12) + x1
            if x < crossing_x:
                inside = not inside
        previous = current
    return inside


def perimeter_score(
    centroid: tuple[float, float] | None,
    polygon: Sequence[tuple[float, float]],
) -> float:
    if centroid is None or not polygon:
        return 0.0
    return 1.0 if point_in_polygon(centroid, polygon) else 0.0


class PassthroughRGBDetector:
    """Adapter used by the CLI and tests until a trained detector is supplied."""

    def score(self, frame: FrameObservation) -> float:
        return clamp(frame.rgb_score)


class PassthroughThermalModel:
    """Adapter used by the CLI and tests until a trained thermal model is supplied."""

    def score(self, frame: ThermalObservation) -> float:
        return clamp(frame.thermal_score)


def motion_magnitude(previous: tuple[float, float] | None, current: tuple[float, float] | None) -> float:
    if previous is None or current is None:
        return 0.0
    return clamp(hypot(current[0] - previous[0], current[1] - previous[1]))
