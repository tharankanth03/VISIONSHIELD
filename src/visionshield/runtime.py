"""One-step runtime bridge from sensor sources and models to the agent."""

from dataclasses import dataclass
from typing import Any

from .agent import VisionShieldAgent
from .models import FrameObservation, ThermalObservation
from .perception import clamp
from .sensors import RGBSource, ThermalSource


@dataclass
class SensorRuntime:
    agent: VisionShieldAgent
    rgb_source: RGBSource
    thermal_source: ThermalSource
    rgb_model: Any
    thermal_model: Any

    def step(self):
        rgb_frame, rgb_timestamp = self.rgb_source.read()
        thermal_frame, thermal_timestamp = self.thermal_source.read()
        if abs((rgb_timestamp - thermal_timestamp).total_seconds()) > 1:
            raise RuntimeError("RGB and thermal captures are more than one second apart.")
        rgb_score = clamp(float(self.rgb_model.score(rgb_frame)))
        detections = tuple(self.rgb_model.detect(rgb_frame)) if hasattr(self.rgb_model, "detect") else ()
        thermal_result = self.thermal_model.analyze(thermal_frame)
        rgb = FrameObservation(
            timestamp=rgb_timestamp,
            rgb_score=rgb_score,
            change_score=0,
            visibility=1,
            source="rgb-camera",
            detections=detections,
        )
        thermal = ThermalObservation(
            timestamp=rgb_timestamp,
            thermal_score=thermal_result.score,
            source="mlx90640",
        )
        return self.agent.process(rgb, thermal)

    def run(self, *, max_steps: int | None = None, on_evidence=None) -> int:
        """Process readings until stopped, returning the number of steps."""
        completed = 0
        try:
            while max_steps is None or completed < max_steps:
                evidence = self.step()
                completed += 1
                if on_evidence is not None:
                    on_evidence(evidence)
        finally:
            self.close()
        return completed

    def close(self) -> None:
        errors = []
        for source in (self.rgb_source, self.thermal_source):
            try:
                source.close()
            except Exception as exc:
                errors.append(exc)
        if errors:
            raise RuntimeError("One or more sensor sources failed to close.") from errors[0]
