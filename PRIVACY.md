# Privacy Policy

**Effective date:** 2026-09-26

VISIONSHIELD is currently a local research and planning archive, not an online service. This policy describes the privacy principles that must govern any future implementation; it does not authorize collection of personal data.

## Data handling

A future implementation may process camera frames, thermal sensor readings, event metadata, and user-provided perimeter configuration on an edge device. It should collect only what is necessary for the configured purpose, keep processing local by default, and avoid sending sensor data to third parties unless the operator has provided clear notice and authorization.

## Retention and deletion

Operators should define a short retention period before enabling event recording. Stored frames, thermal arrays, event metadata, logs, and backups should be deletable by an authorized operator. The system should not retain data indefinitely by default.

## Access and security

Future implementations must protect local storage and dashboard access, separate operator roles where needed, avoid hard-coded credentials, and document security updates. Secrets belong in local configuration and must never be committed to this repository.

## People and rights

Operators are responsible for lawful installation, consent and notice requirements, access requests, deletion requests, and compliance with applicable privacy and surveillance laws. Do not use this project to make decisions about a person's identity, eligibility, or rights.

## Changes and contact

This policy should be updated when an executable implementation, remote service, or new data flow is introduced. No public data-controller contact address has been configured for this research archive.
