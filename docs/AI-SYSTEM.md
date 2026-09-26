# VISIONSHIELD AI system

The working system is composed of optional model adapters around a deterministic core.

| Capability | Working component | Production requirement |
| --- | --- | --- |
| RGB object detection | `YOLODetector` adapter | A licensed, locally trained `.pt` model |
| Thermal anomaly | `ThermalAnomalyDetector` baseline | Representative empty-scene frames and calibration |
| Perimeter analysis | Point-in-polygon `PerimeterDecision` | Camera coordinate calibration |
| Evidence fusion | Visibility-aware weighted fusion | Held-out threshold calibration |
| Phone alerts | Telegram Bot API notifier | Bot token and chat ID stored outside Git |
| Interface | Local HTML dashboard and JSON API | Real camera/thermal adapters |
| Event history | Retention-aware local JSONL store | Choose retention before deployment |
| Sensor runtime | OpenCV/MLX90640 adapters with timestamp guard | Configure real devices and calibration |

The repository does not claim a trained model or measured accuracy without your labeled dataset. Use `scripts/train_yolo.py` for training and `scripts/fit_thermal_baseline.py` for a thermal baseline. Record each released model in `docs/MODEL-GOVERNANCE.md`.

The default runtime remains usable without optional AI packages, model downloads, camera access, or network access.
