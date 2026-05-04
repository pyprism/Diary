#!/usr/bin/env bash
set -euo pipefail

# run from project root (adjust if script lives elsewhere)
cd "$(dirname "$0")"

# Ensure .env exists and load it
if [[ ! -f .env ]]; then
  echo ".env file not found!"
  exit 1
fi
set -a
source .env
set +a
echo "Environment variables loaded from .env file."

if [[ -x ".venv/bin/python" ]]; then
  PYTHON_BIN=".venv/bin/python"
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
else
  PYTHON_BIN="python"
fi

# Ensure background processes are killed when the script exits
cleanup() {
  echo "Shutting down background processes..."
  kill -TERM "${BEAT_PID:-}" "${CELERY_PID:-}" 2>/dev/null || true
  wait "${BEAT_PID:-}" "${CELERY_PID:-}" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

"$PYTHON_BIN" manage.py makemigrations
"$PYTHON_BIN" manage.py migrate

# Start Celery worker in background using same python interpreter.
# Set RUN_CELERY_WORKER=false to run only the API server.
if [[ "${RUN_CELERY_WORKER:-true}" == "true" ]]; then
  "$PYTHON_BIN" -m celery -A hiren worker \
    --loglevel=info \
    --pool=solo \
    --concurrency=1 \
    --without-gossip \
    --without-mingle \
    --without-heartbeat &
  CELERY_PID=$!
fi

# Optional: start celery beat (uncomment to enable)
# python -m celery -A hiren beat --loglevel=info &
# BEAT_PID=$!

"$PYTHON_BIN" manage.py runserver
#pytest -vv -s
#pytest --cov=. --cov-report=html
