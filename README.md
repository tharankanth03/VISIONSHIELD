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
```

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

## Architecture

Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/AI-IMPLEMENTATION.md](docs/AI-IMPLEMENTATION.md) for the contracts, data flow, invariants, and integration plan.

## Responsible deployment

Before connecting sensors, define consent and notice, retention and deletion, operator access, failure behavior, and applicable law. Do not use an unvalidated system for emergency response or decisions about a person's identity, eligibility, or rights. See [PRIVACY.md](PRIVACY.md) and [TERMS.md](TERMS.md).

## Repository status

The orchestration foundation is implemented and tested. Hardware adapters, trained models, production persistence, notifications, and measured evaluation results are intentionally not included yet. No API keys, secrets, datasets, recordings, or model weights belong in this repository.

## License and supplied research

No license has been asserted for the supplied third-party research papers, documents, or images. Confirm provenance, attribution, and redistribution terms before publishing or packaging those files.
