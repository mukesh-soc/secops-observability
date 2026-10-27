# SecOps Observability Platform

A containerized monitoring stack for a Flask API, with security-focused metrics and alerts.

**Stack:** Flask API, Prometheus, Alertmanager, Grafana (auto-provisioned), node-exporter, cAdvisor, GitHub Actions CI with Trivy scanning.

## Run it

```bash
cp .env.example .env     # then edit the passwords
make up                  # docker compose up -d --build
make load                # 2 min of traffic incl. simulated brute-force
```

| Service       | URL                    |
|---------------|------------------------|
| Task API      | http://localhost:8000  |
| Prometheus    | http://localhost:9090  |
| Alertmanager  | http://localhost:9093  |
| Grafana       | http://localhost:3001  |

Grafana opens with the Prometheus data source and the **SecOps Overview** dashboard already loaded (folder: SecOps).

## What's DevSecOps about it
- Non-root, read-only container, all capabilities dropped, `no-new-privileges`
- Secrets via `.env` (compose refuses to start without them), nothing hard-coded
- Security response headers on every reply
- `auth_failures_total` metric + `PossibleBruteForce` alert
- CI: lint, tests, Trivy filesystem and image scans (fail on HIGH/CRITICAL), push to GHCR
- Pinned image versions

## Deploy to a server (any Ubuntu VM)
```bash
git clone <your-repo> && cd secops-observability
cp .env.example .env && nano .env
docker compose up -d --build
```
Open ports 3001 (and 8000 if public). Keep 9090/9093 closed or behind a reverse proxy with TLS (Caddy/Nginx) and auth. Replace the placeholder webhook in `alertmanager/alertmanager.yml` with Slack/email.

## Test
`make test`

## Reset
`make reset` (removes volumes)
