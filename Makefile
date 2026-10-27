.PHONY: up down reset test logs load lint
up:    ; docker compose up -d --build
down:  ; docker compose down
reset: ; docker compose down -v
logs:  ; docker compose logs -f
load:  ; ./scripts/load.sh 120 
lint:  ; pip install -q flake8 && flake8 app --max-line-length=100
test:  ; pip install -q -r app/requirements.txt pytest && pytest -q tests
