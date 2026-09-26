# VISIONSHIELD privacy policy

**Effective date:** 2026-09-27

VISIONSHIELD is a local-first research and edge-AI project. This policy defines the minimum privacy behavior required before connecting a camera, thermal sensor, or phone alert channel.

## Data minimization

The runtime should process only the frames, thermal readings, object labels, and event metadata required for the configured purpose. Raw frames and thermal arrays must stay on the edge by default. Telegram receives only the configured text alert unless an operator explicitly adds another transport.

## Retention and deletion

The operator must choose a retention period before enabling recording. Events, frames, thermal arrays, logs, backups, and exported alerts must have documented deletion procedures. Retention is not permission to keep data indefinitely.

## People and consent

Operators are responsible for notice, consent, lawful use, access requests, deletion requests, and applicable surveillance and data-protection law. VISIONSHIELD must not be used to identify people or make decisions about a person's rights, eligibility, employment, housing, healthcare, or safety.

## Security

Bot tokens, model paths, camera credentials, and local configuration belong outside Git. Dashboard access should be restricted to a trusted local network or protected behind an authenticated gateway before remote access is enabled.

## Changes

Update this policy when a new sensor, cloud service, retention path, notification provider, or personally identifying feature is introduced.
