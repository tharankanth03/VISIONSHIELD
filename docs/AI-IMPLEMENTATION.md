# AI implementation notes

## Scope

The supplied implementation plan describes an edge-first, multimodal pipeline for RGB and low-resolution thermal sensing. It recommends independent perception modules and evidence-level fusion so that a degraded sensor does not receive unqualified trust.

The following boundaries are proposed for a future implementation:

| Component | Proposed approach | Training status |
| --- | --- | --- |
| RGB detector | Lightweight, edge-compatible object detector | Select and validate on project data |
| Thermal analysis | Small model or statistical activity detector for 32×24 MLX90640 frames | Requires project-specific thermal data |
| Visibility | Sharpness, contrast, brightness, and edge-density signals | Conventional computer vision |
| Temporal change | Stabilization, background comparison, and persistence filtering | Conventional computer vision |
| Perimeter | User-defined polygon and centroid/bounding-box intersection checks | Deterministic |
| Evidence fusion | Weighted, visibility-aware score with a confirmation state machine | Tune only against a validation set |
| Dashboard | Local display of sensor health, evidence, and event metadata | Not implemented |

## Agent and model policy

Any future AI agent must be constrained to the repository's documented interfaces and must not invent detections, confidence values, sensor readings, evaluation results, or notifications. Agent outputs should include provenance and timestamps where applicable, and uncertain results should remain explicitly uncertain.

Model weights, datasets, recordings, local databases, credentials, and runtime configuration must remain outside version control unless their redistribution rights and privacy implications have been reviewed. The repository's `.gitignore` excludes common secret, recording, dataset, database, and model-weight patterns.

The proposed event path is:

`RGB + thermal inputs → independent evidence → visibility-aware fusion → persistence check → event record`

Fusion weights and thresholds must be measured on a held-out validation set. They must not be chosen to produce a desired success rate, and this repository currently contains no validated metrics.

## Implementation gate

Before calling the system production-ready, add executable source, pinned dependencies, tests for each module, an evaluation protocol, data-retention controls, and reproducible build/deployment instructions. Until then, this document is an implementation guide only.
