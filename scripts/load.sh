#!/usr/bin/env bash
# Generate traffic so dashboards and alerts have data. Usage: ./scripts/load.sh [seconds]
URL=${URL:-http://localhost:8000}
END=$((SECONDS + ${1:-120}))
while [ $SECONDS -lt $END ]; do
  curl -s "$URL/" >/dev/null
  curl -s -X POST "$URL/api/tasks" -H 'Content-Type: application/json' -d '{"title":"demo"}' >/dev/null
  curl -s "$URL/slow" >/dev/null &
  [ $((RANDOM % 5)) -eq 0 ] && curl -s "$URL/error" >/dev/null
  # simulated brute-force: trips the PossibleBruteForce alert
  for _ in 1 2 3; do
    curl -s -X POST "$URL/login" -H 'Content-Type: application/json' \
      -d '{"username":"admin","password":"guess"}' >/dev/null
  done
  sleep 0.5
done
wait
