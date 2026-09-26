# VISIONSHIELD

VISIONSHIELD is a privacy-conscious, edge-oriented multimodal agent for combining RGB and thermal evidence. It is designed for transparent, local-first event reasoning—not for unvalidated surveillance claims.

## What is included

- Typed RGB and thermal observation contracts.
- Pluggable `RGBDetector` and `ThermalModel` interfaces.
- Perimeter context and bounded score validation.
- Visibility-aware weighted evidence fusion.
- Persistent `clear → candidate → confirmed` event state machine.
- Deterministic, minimal event records.
- Plain-text phone alerts through an optional Telegram bot integration.
- Optional Ultralytics YOLO adapter and reproducible training entry point.
- Dependency-free thermal anomaly baseline and perimeter decision module.
- Local HTML control UI with JSON observation API.
- Retention-aware local JSONL event history with health and history endpoints.
- Isolated OpenCV and MLX90640 sensor adapters plus a timestamp-safe runtime bridge.
- Explicit hardware command that refuses missing weights/baselines instead of silently using simulator data.
- GitHub Actions CI across Python 3.10–3.12.
- JSON configuration example and a dependency-free CLI smoke run.
- Architecture, AI implementation, privacy, and terms documentation.

The supplied research papers, planning documents, and image files remain preserved at the repository root. They are source material, not evidence of implemented performance.

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
python -m unittest discover -s tests -v
visionshield --config config.example.json
visionshield-ui
```

Open `http://127.0.0.1:8080` for the local control UI. Its simulator form exercises the same state/fusion pipeline; connect real camera and thermal adapters before treating it as live sensor data.

The local API also exposes `GET /api/health`, `GET /api/status`, and `GET /api/events`. Confirmed events are stored as minimal JSONL records under `events/` and are automatically removed after `retention_seconds`.

The UI's recent-events panel shows the object label, model confidence, fusion score, UTC timestamp, and event ID for confirmed events.

For hardware integration, use `OpenCVCameraSource`, `MLX90640Source`, and `SensorRuntime`. Hardware timestamps must be within one second or the runtime rejects the pair instead of fusing stale readings.

The intended hardware launch shape is:

```bash
visionshield-hardware --config config.local.json --weights models/yolo.pt --thermal-baseline models/thermal-baseline.json
```

The command validates local model assets and stops with an explicit message until a board-specific MLX90640 bus reader is supplied. This is deliberate: sensor libraries differ by board and the project must not pretend to read hardware it cannot access.

The example configuration is schema-validated at load time, including hardware, fusion, notification, retention, and perimeter settings. Invalid thresholds, weights, frame sizes, or sensor timing fail explicitly.

## AI models and training

Install optional model dependencies only when you are ready to supply data:

```bash
python -m pip install -e .[ai]
python scripts/train_yolo.py --data path/to/visionshield.yaml --epochs 50
```

The `YOLODetector` adapter loads a trained local `.pt` file and returns object labels and calibrated confidence values. The repository does not include weights and cannot honestly train a detector without a labeled, consented dataset. For thermal anomaly detection, fit a baseline from newline-delimited thermal frames:

```bash
python scripts/fit_thermal_baseline.py thermal-baseline.jsonl thermal-model.json
```

The baseline is a working statistical fallback, not a learned person classifier. Keep datasets, weights, recordings, and generated `runs/` outside Git.

The default CLI uses deterministic passthrough scores to exercise orchestration. It reports a sample `person` label only because the CLI input supplies that label; it does not claim to detect people. Replace those adapters only after validating real camera and thermal models.

## Phone alerts

Telegram is the simplest supported phone integration. Create a Telegram bot with `@BotFather`, send the bot one message, obtain the target chat ID, and place the values in a local config file (never commit the real token):

```json
{
  "notifications": {
    "telegram_bot_token": "YOUR_BOT_TOKEN",
    "telegram_chat_id": "YOUR_CHAT_ID",
    "timeout_seconds": 10
  }
}
```

When RGB and thermal evidence remain above the configured threshold, the agent sends one plain-text alert on the transition to `confirmed`. The message includes the detected object labels and confidence, RGB evidence, thermal sensor status, fusion score, event ID, and UTC time. Alerts are disabled when either setting is blank. Network failures are raised explicitly rather than silently treated as delivered.

The default `cooldown_seconds` value prevents repeated alerts while the same event remains confirmed. Set it to `0` only when every confirmed transition should be delivered to the phone.

## Project documentation

Read [docs/SYSTEM-ARCHITECTURE.md](docs/SYSTEM-ARCHITECTURE.md), [docs/AI-SYSTEM.md](docs/AI-SYSTEM.md), and [docs/MODEL-GOVERNANCE.md](docs/MODEL-GOVERNANCE.md) for the system design and model controls.

## Responsible deployment

Before connecting sensors, define consent and notice, retention and deletion, operator access, failure behavior, and applicable law. Do not use an unvalidated system for emergency response or decisions about a person's identity, eligibility, or rights. See [docs/PRIVACY-POLICY.md](docs/PRIVACY-POLICY.md) and [docs/TERMS-OF-USE.md](docs/TERMS-OF-USE.md).

Security concerns belong in [SECURITY.md](SECURITY.md); contribution rules are in [CONTRIBUTING.md](CONTRIBUTING.md).

## Repository status

The orchestration foundation is implemented and tested. Hardware adapters, trained models, production persistence, notifications, and measured evaluation results are intentionally not included yet. No API keys, secrets, datasets, recordings, or model weights belong in this repository.

## License and supplied research

No license has been asserted for the supplied third-party research papers, documents, or images. Confirm provenance, attribution, and redistribution terms before publishing or packaging those files.
