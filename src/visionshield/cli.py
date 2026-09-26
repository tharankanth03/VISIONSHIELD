"""Command-line entry point for a deterministic agent smoke run."""

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from .agent import VisionShieldAgent
from .config import AgentConfig
from .models import FrameObservation, ObjectDetection, ThermalObservation
from .notifier import NullNotifier, TelegramNotifier


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a VISIONSHIELD multimodal evidence check.")
    parser.add_argument("--config", type=Path, help="Path to a JSON agent configuration.")
    parser.add_argument("--rgb-score", type=float, default=0.8)
    parser.add_argument("--thermal-score", type=float, default=0.8)
    parser.add_argument("--visibility", type=float, default=1.0)
    parser.add_argument("--change-score", type=float, default=0.7)
    parser.add_argument("--x", type=float, default=0.5)
    parser.add_argument("--y", type=float, default=0.5)
    parser.add_argument("--object", dest="object_label", default="person")
    parser.add_argument("--object-confidence", type=float, default=0.8)
    args = parser.parse_args()
    config = AgentConfig.from_json(args.config) if args.config else AgentConfig()
    notifier = TelegramNotifier(
        config.notifications.telegram_bot_token,
        config.notifications.telegram_chat_id,
        config.notifications.timeout_seconds,
    ) if config.notifications.enabled else None
    agent = VisionShieldAgent(config, notifier=notifier or NullNotifier())
    timestamp = datetime.now(timezone.utc)
    rgb = FrameObservation(
        timestamp, args.rgb_score, args.change_score, args.visibility, (args.x, args.y),
        detections=(ObjectDetection(args.object_label, args.object_confidence),),
    )
    thermal = ThermalObservation(timestamp, args.thermal_score)
    evidence = agent.process(rgb, thermal)
    print(json.dumps(evidence.as_dict(), indent=2))
