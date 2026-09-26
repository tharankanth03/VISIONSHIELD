# VISIONSHIELD

VISIONSHIELD is a privacy-conscious, edge-oriented multimodal agent for combining RGB and thermal evidence. It is designed for transparent, local-first event reasoning—not for unvalidated surveillance claims.

## What is included

- Typed RGB and thermal observation contracts.
- Pluggable `RGBDetector` and `ThermalModel` interfaces.
- Perimeter context and bounded score validation.
- Visibility-aware weighted evidence fusion.
- Persistent `clear → candidate → confirmed` event state machine.
- Deterministic, minimal event records.
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

The default CLI uses deterministic passthrough scores to exercise orchestration. It does not claim to detect people or objects. Replace those adapters only after validating real camera and thermal models.

## Architecture

Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) and [docs/AI-IMPLEMENTATION.md](docs/AI-IMPLEMENTATION.md) for the contracts, data flow, invariants, and integration plan.

## Responsible deployment

Before connecting sensors, define consent and notice, retention and deletion, operator access, failure behavior, and applicable law. Do not use an unvalidated system for emergency response or decisions about a person's identity, eligibility, or rights. See [PRIVACY.md](PRIVACY.md) and [TERMS.md](TERMS.md).

## Repository status

The orchestration foundation is implemented and tested. Hardware adapters, trained models, production persistence, notifications, and measured evaluation results are intentionally not included yet. No API keys, secrets, datasets, recordings, or model weights belong in this repository.

## License and supplied research

No license has been asserted for the supplied third-party research papers, documents, or images. Confirm provenance, attribution, and redistribution terms before publishing or packaging those files.
