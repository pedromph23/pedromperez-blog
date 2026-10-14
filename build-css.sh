#!/usr/bin/env bash
# =============================================================
# build-css.sh
# Compila Tailwind y hace stage del CSS resultante.
# Uso: ./build-css.sh
# =============================================================
set -euo pipefail

cd "$(dirname "$0")"

# Activar venv si no está activo
if [[ -z "${VIRTUAL_ENV:-}" ]]; then
    source .venv/bin/activate
fi

echo "==> Compilando Tailwind CSS..."
python manage.py tailwind build

echo "==> Añadiendo CSS a git staging..."
git add -f theme/static/css/dist/styles.css

# Tamaño del archivo
SIZE=$(wc -c < theme/static/css/dist/styles.css)
echo "==> CSS compilado: $SIZE bytes"
echo "==> Listo. Ahora haz: git commit -m 'tu mensaje' && git push"
