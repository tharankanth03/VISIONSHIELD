"""Fit a baseline anomaly detector from newline-delimited thermal frames."""

import argparse
import json
from pathlib import Path

from visionshield.anomaly import ThermalAnomalyDetector


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="JSONL file; each line is an array of temperatures.")
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    frames = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    detector = ThermalAnomalyDetector.fit(frames)
    args.output.write_text(json.dumps({"baseline_mean": detector.baseline_mean, "baseline_std": detector.baseline_std}), encoding="utf-8")


if __name__ == "__main__":
    main()
