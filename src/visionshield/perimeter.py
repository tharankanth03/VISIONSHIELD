"""Perimeter configuration and state reporting."""

from dataclasses import dataclass
from typing import Sequence

from .perception import perimeter_score


@dataclass(frozen=True)
class PerimeterDecision:
    inside: bool
    score: float
    configured: bool


def evaluate(
    centroid: tuple[float, float] | None,
    polygon: Sequence[tuple[float, float]],
) -> PerimeterDecision:
    configured = bool(polygon)
    score = perimeter_score(centroid, polygon)
    return PerimeterDecision(bool(score), score, configured)
