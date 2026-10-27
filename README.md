# Observability Lab: Prometheus & Grafana

- `lab-stack/`: the project exactly as written in the lab manual (Prometheus + Grafana, ports 9090/3001).
- `secops-observability/`: my own extended project (instrumented API, alerts, provisioned dashboards, CI/security scanning).

Both use Grafana on port 3001, so run one at a time (`docker compose down` in the other first).
