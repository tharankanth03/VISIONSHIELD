"""Dependency-free anomaly scoring for thermal frames.

This is a calibrated statistical baseline, not a neural network. It provides
a working fallback while a project-specific anomaly model is trained.
"""

from dataclasses import dataclass
from math import sqrt
from statistics import mean, pstdev
from typing import Iterable

from .perception import clamp


@dataclass(frozen=True)
class AnomalyResult:
    score: float
    mean_temperature: float
    deviation: float
    active: bool


@dataclass
class ThermalAnomalyDetector:
    """Compare a thermal frame against a learned baseline distribution."""

    baseline_mean: float
    baseline_std: float
    activation_z: float = 2.5

    def __post_init__(self) -> None:
        if self.baseline_std <= 0:
            raise ValueError("baseline_std must be positive.")
        if self.activation_z <= 0:
            raise ValueError("activation_z must be positive.")

    @classmethod
    def fit(cls, frames: Iterable[Iterable[float]], activation_z: float = 2.5) -> "ThermalAnomalyDetector":
        values = [float(value) for frame in frames for value in frame]
        if len(values) < 2:
            raise ValueError("At least two thermal values are required to fit a baseline.")
        return cls(mean(values), max(pstdev(values), 0.01), activation_z)

    def analyze(self, frame: Iterable[float]) -> AnomalyResult:
        values = [float(value) for value in frame]
        if not values:
            raise ValueError("Thermal frame cannot be empty.")
        current_mean = mean(values)
        z_score = abs(current_mean - self.baseline_mean) / self.baseline_std
        score = clamp(z_score / (self.activation_z * 2))
        return AnomalyResult(score, current_mean, z_score, z_score >= self.activation_z)
