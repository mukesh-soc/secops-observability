# Lab Stack: Prometheus + Grafana

Exactly the stack from the lab manual.

```bash
docker compose up -d
docker compose ps
```

- Prometheus: http://localhost:9090  (Status -> Targets, query `up`)
- Grafana:    http://localhost:3001  (admin / admin)
  - Data source URL: `http://prometheus:9090` (service name, not localhost)
  - Import dashboard ID `3662`

Teardown: `docker compose down` (keeps data) or `docker compose down -v` (wipes volumes).
