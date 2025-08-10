#!/usr/bin/env bash
set -Eeuo pipefail

# 1) Pararse donde está manage.py (si ya estás ahí, no pasa nada)
if [ -f "./manage.py" ]; then
  ROOT="."
else
  ROOT="$(dirname "$(find . -maxdepth 3 -type f -name manage.py -not -path "*/.venv/*" | head -n1)")"
  cd "$ROOT"
fi

# 2) Tareas previas (opcionales). Podés desactivar con RUN_COLLECTSTATIC=0 o RUN_MIGRATIONS=0
: "${RUN_COLLECTSTATIC:=1}"
: "${RUN_MIGRATIONS:=1}"

if [ "$RUN_COLLECTSTATIC" = "1" ]; then
  python manage.py collectstatic --noinput
fi

if [ "$RUN_MIGRATIONS" = "1" ]; then
  python manage.py migrate --noinput
fi

# 3) Detectar si es ASGI o WSGI leyendo settings (genérico para cualquier proyecto)
ASGI_APP="$(python manage.py shell -c 'from django.conf import settings; print(getattr(settings, "ASGI_APPLICATION", ""))' || true)"

if [ -n "$ASGI_APP" ]; then
  # ASGI (Channels/FastAPI híbridos, etc.)
  exec uvicorn "$ASGI_APP" --host 0.0.0.0 --port "${PORT:-8000}"
else
  # WSGI (Django clásico)
  WSGI_APP="$(python manage.py shell -c 'from django.conf import settings; print(settings.WSGI_APPLICATION)')"
  exec gunicorn "$WSGI_APP" --bind "0.0.0.0:${PORT:-8000}"
fi
