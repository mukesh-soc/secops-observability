#!/usr/bin/env bash
# One-shot setup for a fresh Ubuntu 22.04/24.04 VM.
# Usage: curl -fsSL https://raw.githubusercontent.com/mukesh-soc/secops-observability/main/scripts/bootstrap-vm.sh | bash
set -euo pipefail
REPO=${REPO:-https://github.com/mukesh-soc/secops-observability.git}
DIR=${DIR:-$HOME/secops-observability}

command -v docker >/dev/null || { curl -fsSL https://get.docker.com | sudo sh; sudo usermod -aG docker "$USER"; }

# Firewall: SSH + web only. Prometheus/Alertmanager stay bound to localhost.
sudo ufw allow OpenSSH >/dev/null && sudo ufw allow 80,443/tcp >/dev/null && sudo ufw --force enable >/dev/null

[ -d "$DIR/.git" ] && git -C "$DIR" pull --ff-only || git clone "$REPO" "$DIR"
cd "$DIR"

if [ ! -f .env ]; then
  gen() { head -c 24 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 20; }
  cat > .env <<ENV
DOMAIN=${DOMAIN:-}
DEMO_USER=admin
DEMO_PASSWORD=$(gen)
GRAFANA_USER=admin
GRAFANA_PASSWORD=$(gen)
ENV
  chmod 600 .env
  echo "Generated .env with random passwords (see $DIR/.env)"
fi

sudo docker compose up -d --build
echo "Done. Grafana: http://<server-ip>/grafana/  (credentials in $DIR/.env)"
