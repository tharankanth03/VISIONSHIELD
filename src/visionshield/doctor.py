"""Safe deployment preflight checks."""

import argparse
import importlib.util
import json
from pathlib import Path

from .config import AgentConfig


def check(config_path: Path, weights: Path | None, baseline: Path | None) -> dict:
    result = {
        "config": {"path": str(config_path), "ok": False},
        "weights": {"path": str(weights) if weights else None, "ok": None},
        "thermal_baseline": {"path": str(baseline) if baseline else None, "ok": None},
        "optional_dependencies": {
            "ultralytics": importlib.util.find_spec("ultralytics") is not None,
            "cv2": importlib.util.find_spec("cv2") is not None,
        },
        "alerts_enabled": False,
        "ready": False,
    }
    try:
        config = AgentConfig.from_json(config_path)
        result["config"]["ok"] = True
        result["alerts_enabled"] = config.notifications.enabled
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as exc:
        result["config"]["error"] = str(exc)
        return result
    if weights is not None:
        result["weights"]["ok"] = weights.is_file() and weights.suffix == ".pt"
    if baseline is not None:
        result["thermal_baseline"]["ok"] = baseline.is_file()
        if result["thermal_baseline"]["ok"]:
            try:
                json.loads(baseline.read_text(encoding="utf-8"))
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                result["thermal_baseline"]["ok"] = False
                result["thermal_baseline"]["error"] = str(exc)
    result["ready"] = (
        result["config"]["ok"]
        and (weights is None or result["weights"]["ok"])
        and (baseline is None or result["thermal_baseline"]["ok"])
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Check VISIONSHIELD configuration without starting hardware.")
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--weights", type=Path)
    parser.add_argument("--thermal-baseline", type=Path)
    args = parser.parse_args()
    result = check(args.config, args.weights, args.thermal_baseline)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["ready"] else 1)


if __name__ == "__main__":
    main()
