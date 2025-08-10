#!/usr/bin/env bash
set -Eeuo pipefail

# 1) Ir a la carpeta del manage.py
if [ -f "./manage.py" ]; then
  ROOT="."
else
  ROOT="$(dirname "$(find . -maxdepth 3 -type f -name manage.py -not -path "*/.venv/*" | head -n1)")"
  cd "$ROOT"
fi

# 2) Tareas previas
python manage.py collectstatic --noinput
python manage.py migrate --noinput

# 3) Leer WSGI_APPLICATION desde settings y lanzar Gunicorn
WSGI_APP="$(python manage.py shell -c 'from django.conf import settings; print(settings.WSGI_APPLICATION)')"
exec gunicorn "$WSGI_APP" --bind "0.0.0.0:${PORT:-8000}"
