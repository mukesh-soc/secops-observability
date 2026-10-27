.PHONY: up down reset test logs load
up:    ; docker compose up -d --build
down:  ; docker compose down
reset: ; docker compose down -v
logs:  ; docker compose logs -f
load:  ; ./scripts/load.sh 120
test:  ; pip install -q -r app/requirements.txt pytest && pytest -q tests
