"""
Entrypoint WSGI para Vercel.
Ejecuta build de Tailwind + collectstatic en el primer arranque (cold start).
"""
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
os.chdir(str(ROOT))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("DJANGO_DEBUG", "False")

# Build on cold start (una sola vez por instancia serverless)
_FLAG = ROOT / ".build_done"
if not _FLAG.exists():
    print("[cold-start] Ejecutando vercel-build.sh...")
    try:
        subprocess.run(
            ["bash", "vercel-build.sh"],
            check=True,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
        _FLAG.touch()
        print("[cold-start] Build completado")
    except subprocess.CalledProcessError as e:
        print(f"[cold-start] Build falló: {e.stderr}")
        raise

from django.core.wsgi import get_wsgi_application  # noqa: E402

app = get_wsgi_application()
