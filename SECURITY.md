# Security Policy

## Reporting a vulnerability
Open a private report via **Security → Report a vulnerability** on this repository.
Please do not file public issues for security problems.

## Controls in this project
- Non-root, read-only container with all Linux capabilities dropped
- Secrets only via environment (`.env`, git-ignored); compose refuses to start without them
- Prometheus/Alertmanager bound to localhost; only Caddy (80/443) is public
- `/metrics` blocked at the reverse proxy
- Trivy (vulns, secrets, misconfig), CodeQL and Dependabot in CI
- Pinned image and dependency versions
