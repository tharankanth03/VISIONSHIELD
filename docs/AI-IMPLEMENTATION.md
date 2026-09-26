# AI implementation

VISIONSHIELD is now an executable multimodal agent foundation, not a marketing website. The agent coordinates RGB evidence, thermal evidence, deterministic scene context, visibility-aware fusion, and a persistent event state machine.

## Current implementation

| Layer | Implementation | Boundary |
| --- | --- | --- |
| Input contracts | Typed RGB and thermal observations | Requires real sensor adapters |
| RGB model | `RGBDetector` protocol plus deterministic passthrough adapter | Replace with a validated edge detector |
| Thermal model | `ThermalModel` protocol plus deterministic passthrough adapter | Replace with an MLX90640 model |
| Context | Perimeter point-in-polygon and calibrated scores | Add production change/visibility adapters |
| Fusion | Weighted score with visibility-aware RGB reliability | Tune only on held-out validation data |
| Agent | Timestamp validation, persistence, event creation | Add runtime storage/notification consumers |
| Phone alerts | Optional Telegram Bot API notifier | Configure a bot token and chat ID outside Git |

The default adapters accept supplied scores so the orchestration can be tested without pretending a trained model exists. They are not production detectors.

Detected labels come from the RGB model adapter as `ObjectDetection` records. The agent does not infer or invent labels. A confirmed event formats those labels into a plain-text alert together with RGB and thermal sensor status.

## Run locally

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .
python -m unittest discover -s tests -v
visionshield --config config.example.json --object person
```

Telegram alerts are optional and use the standard Bot API over HTTPS. Keep the bot token, chat ID, and all other credentials in a local untracked config file; `config.example.json` contains blanks only. No alert is sent unless both Telegram fields are configured.

## Required next adapters

1. Implement the RGB camera adapter and validate a lightweight detector on representative, consented data.
2. Implement MLX90640 capture, calibration, and a thermal activity model.
3. Add frame-level visibility and temporal change measurements.
4. Add retention-aware event storage and an explicitly authorized notification adapter.
5. Evaluate RGB-only, thermal-only, and fused modes on a held-out dataset; publish measured results rather than assumed metrics.

See [ARCHITECTURE.md](ARCHITECTURE.md) for data flow and invariants.
