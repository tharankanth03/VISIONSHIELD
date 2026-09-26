"""The VISIONSHIELD multimodal orchestration agent."""

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Sequence

from .config import AgentConfig
from .fusion import EventStateMachine, fuse_scores
from .models import Evidence, Event, FrameObservation, ThermalObservation, utc_now
from .notifier import AlertNotifier, NullNotifier
from .perception import (
    PassthroughRGBDetector,
    PassthroughThermalModel,
    RGBDetector,
    ThermalModel,
    perimeter_score,
)


@dataclass
class VisionShieldAgent:
    """Coordinate RGB, thermal, context, fusion, and event output."""

    config: AgentConfig = field(default_factory=AgentConfig)
    rgb_detector: RGBDetector = field(default_factory=PassthroughRGBDetector)
    thermal_model: ThermalModel = field(default_factory=PassthroughThermalModel)
    notifier: AlertNotifier = field(default_factory=NullNotifier)
    state_machine: EventStateMachine = field(init=False)
    _history: list[float] = field(default_factory=list, init=False)
    _event_sequence: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        self.state_machine = EventStateMachine(self.config.fusion)

    def process(
        self, rgb: FrameObservation, thermal: ThermalObservation
    ) -> Evidence:
        if thermal.timestamp != rgb.timestamp:
            raise ValueError("RGB and thermal observations must have the same timestamp.")
        rgb_score = self.rgb_detector.score(rgb)
        thermal_score = self.thermal_model.score(thermal)
        perimeter = perimeter_score(rgb.centroid, self.config.perimeter)
        persistence = self._persistence()
        score, explanations = fuse_scores(
            rgb=rgb_score,
            thermal=thermal_score,
            change=rgb.change_score,
            perimeter=perimeter,
            persistence=persistence,
            visibility=rgb.visibility,
            config=self.config.fusion,
        )
        previous_state = self.state_machine.state
        state = self.state_machine.transition(score)
        self._history.append(score)
        self._history = self._history[-self.config.fusion.required_confirmations :]
        evidence = Evidence(
            timestamp=rgb.timestamp,
            rgb=rgb_score,
            thermal=thermal_score,
            change=rgb.change_score,
            perimeter=perimeter,
            persistence=persistence,
            visibility=rgb.visibility,
            score=score,
            state=state,
            explanations=explanations,
            detected_objects=rgb.detections,
            thermal_active=thermal_score >= self.config.fusion.thermal_activation_threshold,
        )
        if previous_state != state and state.value == "confirmed":
            event = self.create_event(evidence)
            self.notifier.send(self.notifier.format_event(event))
        return evidence

    def create_event(self, evidence: Evidence, metadata: dict | None = None) -> Event:
        if evidence.state.value != "confirmed":
            raise ValueError("Only confirmed evidence can create an event.")
        self._event_sequence += 1
        raw_id = f"{evidence.timestamp.isoformat()}:{self._event_sequence}"
        event_id = sha256(raw_id.encode("utf-8")).hexdigest()[:16]
        return Event(event_id, evidence.timestamp, evidence, metadata or {})

    def _persistence(self) -> float:
        required = self.config.fusion.required_confirmations
        if not self._history:
            return 0.0
        return min(1.0, len(self._history) / required)

    @property
    def state(self):
        return self.state_machine.state
