# VISIONSHIELD

VISIONSHIELD is a research and planning archive for a privacy-conscious, edge-oriented RGB and thermal monitoring system. This repository preserves the supplied planning documents, research references, and image assets for the proposed **NIGHTJAR–VISIONSHIELD-X** implementation.

## Repository status

This repository currently contains planning and research material only. It does **not** contain an executable application, package manifest, trained model, deployment configuration, or production build script. No performance, detection accuracy, alert rate, or other product metric is asserted here.

The duplicate files supplied with the project are retained as supplied so that no user material is silently discarded. Before implementation, the project should establish provenance and licensing for each research paper, image, and other third-party asset.

## Intended implementation

The implementation plan proposes a modular edge pipeline rather than one large RGB-thermal model:

1. Capture and preprocess RGB camera and MLX90640 thermal data.
2. Run lightweight RGB detection, thermal activity analysis, temporal change detection, visibility estimation, and perimeter checks independently.
3. Combine evidence with visibility-aware, rule-based fusion.
4. Require persistent, multi-signal evidence before creating an event.
5. Store a minimal event record and expose status through a local dashboard.

This is a design direction, not an implemented or validated feature list. See [docs/AI-IMPLEMENTATION.md](docs/AI-IMPLEMENTATION.md) for the proposed agent and model boundaries.

## Supplied material

The root-level PDFs, DOCX planning files, and PNG assets are the original supplied project files. They are intentionally left in place. The planning documents are the authoritative source for the proposed V1 architecture until an implementation specification replaces them.

## Development

There is currently no package manager manifest or executable source tree, so there is no project-specific build, test, or development command to run. When implementation begins, add the chosen toolchain and document reproducible commands here before claiming production readiness.

## Safety and privacy

This archive is not a surveillance service and does not provide legal, safety, or security advice. Any future implementation must define consent, retention, access control, notification, and deletion behavior before processing camera or thermal data. See [PRIVACY.md](PRIVACY.md) and [TERMS.md](TERMS.md).

## License

No license has been asserted for the supplied research papers, documents, or image assets. Do not redistribute third-party material until its license and attribution requirements have been confirmed.
