#!/usr/bin/env bash
set -euo pipefail

# example commands:
# ./scripts/dockerless_run.sh makemigrations
# ./scripts/dockerless_run.sh migrate
# ./scripts/dockerless_run.sh runserver
# ./scripts/dockerless_run.sh test
# ./scripts/dockerless_run.sh celery-worker
# ./scripts/dockerless_run.sh celery-beat


ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ -f ".env" ]; then
  set -a
  # shellcheck disable=SC1091
  . ".env"
  set +a
fi


PYTHON="${PYTHON:-$ROOT_DIR/.venv/bin/python}"
COMMAND="${1:-server}"

if [ ! -x "$PYTHON" ]; then
  python3.14 -m venv "$ROOT_DIR/.venv"
  PYTHON="$ROOT_DIR/.venv/bin/python"
fi

if ! "$PYTHON" -c "import django" >/dev/null 2>&1; then
  "$PYTHON" -m pip install --upgrade pip
  "$PYTHON" -m pip install -r requirements.txt
fi

case "$COMMAND" in
  check)
    "$PYTHON" manage.py check
    ;;
  makemigrations)
    "$PYTHON" manage.py makemigrations "${@:2}"
    ;;
  migrate)
    "$PYTHON" manage.py migrate "${@:2}"
    ;;
  server|runserver)
    "$PYTHON" manage.py runserver
    ;;
  celery-worker|worker)
    "$PYTHON" -m celery -A hiren worker \
      --loglevel="${CELERY_LOGLEVEL:-info}" \
      --without-gossip \
      --without-mingle \
      --without-heartbeat \
      "${@:2}"
    ;;
  celery-beat|beat)
    "$PYTHON" -m celery -A hiren beat --loglevel="${CELERY_LOGLEVEL:-info}" "${@:2}"
    ;;
  celery)
    "$PYTHON" -m celery -A hiren "${@:2}"
    ;;
  test)
    "$PYTHON" -m pytest -vv
    ;;
  *)
    "$PYTHON" manage.py "$@"
    ;;
esac
