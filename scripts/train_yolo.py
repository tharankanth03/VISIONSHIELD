"""Train a YOLO detector from a dataset YAML.

Usage: python scripts/train_yolo.py --data data/visionshield.yaml --epochs 50
The dataset and generated weights are intentionally not committed.
"""

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--model", default="yolo11n.pt")
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--imgsz", type=int, default=640)
    args = parser.parse_args()
    if not args.data.exists():
        raise SystemExit(f"Dataset YAML not found: {args.data}")
    try:
        from ultralytics import YOLO
    except ImportError as exc:
        raise SystemExit("Install training dependencies with: pip install -e .[ai]") from exc
    model = YOLO(args.model)
    model.train(data=str(args.data), epochs=args.epochs, imgsz=args.imgsz, project="runs", name="visionshield")


if __name__ == "__main__":
    main()
