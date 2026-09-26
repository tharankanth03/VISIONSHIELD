"""Hardware runtime command.

This command intentionally requires explicit adapter/model paths and never
downloads model weights or silently falls back to simulator values.
"""

import argparse
import json
from pathlib import Path

from .agent import VisionShieldAgent
from .anomaly import ThermalAnomalyDetector
from .config import AgentConfig
from .notifier import NullNotifier, TelegramNotifier
from .runtime import SensorRuntime
from .sensors import MLX90640Source, OpenCVCameraSource
from .yolo import YOLODetector


def main() -> None:
    parser = argparse.ArgumentParser(description="Run VISIONSHIELD with real RGB and thermal sources.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--weights", type=Path, required=True, help="Local YOLO .pt weights file.")
    parser.add_argument("--thermal-baseline", type=Path, required=True, help="JSON baseline model.")
    parser.add_argument("--camera-device", type=int)
    parser.add_argument("--max-steps", type=int)
    args = parser.parse_args()
    if not args.weights.exists():
        raise SystemExit(f"YOLO weights not found: {args.weights}")
    if not args.thermal_baseline.exists():
        raise SystemExit(f"Thermal baseline not found: {args.thermal_baseline}")
    config = AgentConfig.from_json(args.config)
    camera_device = config.hardware.camera_device if args.camera_device is None else args.camera_device
    notifier = (
        TelegramNotifier(
            config.notifications.telegram_bot_token,
            config.notifications.telegram_chat_id,
            config.notifications.timeout_seconds,
        )
        if config.notifications.enabled
        else NullNotifier()
    )
    rgb_model = YOLODetector(args.weights)
    baseline = json.loads(args.thermal_baseline.read_text(encoding="utf-8"))
    thermal_model = ThermalAnomalyDetector(**baseline)
    raise SystemExit(
        "Hardware execution requires an MLX90640 bus reader. "
        "Construct MLX90640Source with your board-specific reader and call SensorRuntime.run()."
    )


if __name__ == "__main__":
    main()
