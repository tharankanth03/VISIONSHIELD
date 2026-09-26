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
        thermal_result = self.thermal_model.analyze(thermal_frame)
        rgb = FrameObservation(
            timestamp=rgb_timestamp,
            rgb_score=rgb_score,
            change_score=0,
            visibility=1,
            source="rgb-camera",
        )
        thermal = ThermalObservation(
            timestamp=rgb_timestamp,
            thermal_score=thermal_result.score,
            source="mlx90640",
        )
        return self.agent.process(rgb, thermal)

    def close(self) -> None:
        self.rgb_source.close()
        self.thermal_source.close()
