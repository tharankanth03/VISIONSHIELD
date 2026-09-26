# Model governance

## Required model record

Every production model must have a record containing:

- model name, version, source, and license;
- training dataset provenance and consent status;
- classes and label definitions;
- hardware/runtime version;
- confidence threshold and calibration method;
- held-out evaluation results and known failure cases;
- rollback path and review owner.

## YOLO policy

The YOLO adapter never downloads weights implicitly. A local `.pt` file must be supplied and its license and checksum recorded. Training uses `scripts/train_yolo.py` with a project-specific dataset YAML. CI does not train or publish weights.

## Thermal anomaly policy

The baseline anomaly detector measures deviation from an empty-scene distribution. It does not identify people, classify intent, or establish that an alert is true. Baseline data must represent the expected operating environment and be periodically reviewed after sensor placement changes.

## Release gate

Do not promote a model to production until it has been evaluated on held-out data, its false-alert behavior is understood, and its output is reviewed with the privacy policy and alert escalation rules.
