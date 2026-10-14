#!/usr/bin/env bash
# =============================================================
# vercel-build.sh
# Script de build para Vercel: compila Tailwind + collectstatic
# =============================================================
set -euo pipefail

echo "==> [1/3] Instalando binario de Tailwind..."
python manage.py tailwind install

echo "==> [2/3] Compilando Tailwind CSS..."
python manage.py tailwind build

echo "==> [3/3] Recopilando archivos estáticos..."
python manage.py collectstatic --noinput --clear

echo "==> Build completado exitosamente"
