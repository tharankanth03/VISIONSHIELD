"""VISIONSHIELD multimodal edge evidence agent."""

from .agent import VisionShieldAgent
from .config import AgentConfig
from .models import Evidence, Event, FrameObservation, ObjectDetection, ThermalObservation
from .notifier import TelegramNotifier

__all__ = [
    "AgentConfig",
    "Evidence",
    "Event",
    "FrameObservation",
    "ObjectDetection",
    "ThermalObservation",
    "TelegramNotifier",
    "VisionShieldAgent",
]
