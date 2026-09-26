# Contributing to VISIONSHIELD

## Development setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e .[dev]
python -m pytest -q
```

Optional AI dependencies are installed separately with `python -m pip install -e .[ai]`.

## Change requirements

Keep core behavior deterministic and dependency-light. Add tests for state transitions, score boundaries, timestamps, alert formatting, and failure paths. Do not commit secrets, generated runs, datasets, recordings, or weights.

Document model and data assumptions in `docs/MODEL-GOVERNANCE.md`. A pull request must state whether a change affects privacy, retention, alert delivery, or model behavior.
