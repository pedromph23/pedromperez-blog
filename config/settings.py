"""
Django settings for pedromperez-blog.
Stack: Django 6.1 + Supabase + Tailwind v4 + whitenoise.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1,.vercel.app"
).split(",")


# Permitir el host que usa el cliente de test de Django
if DEBUG and "testserver" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append("testserver")

# CSRF trusted origins (producción)
CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "http://localhost:8000,https://*.vercel.app"
).split(",")
# --- Aplicaciones ---------------------------------------------------------
INSTALLED_APPS = [
    "axes",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "tailwind",
    "theme",
    # Proyecto
    "blog",
    "projects",
    "core",
]

MIDDLEWARE = [
    "axes.middleware.AxesMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Base de datos --------------------------------------------------------
# Local: SQLite. Producción: Supabase (Postgres) activando USE_SUPABASE=1.
if os.getenv("USE_SUPABASE", "0") == "1":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("SUPABASE_DB_NAME", "postgres"),
            "USER": os.getenv("SUPABASE_DB_USER"),
            "PASSWORD": os.getenv("SUPABASE_DB_PASSWORD"),
            "HOST": os.getenv("SUPABASE_DB_HOST"),
            "PORT": os.getenv("SUPABASE_DB_PORT", "5432"),
            "OPTIONS": {"sslmode": "require"},
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }



# =============================================================
# Override: usar SQLite en tests (evita conflicto con pooler de Supabase)
# =============================================================
import sys as _sys
if "test" in _sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db_test.sqlite3",
    }


# --- Password validation --------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- i18n -----------------------------------------------------------------
LANGUAGE_CODE = "es-ve"
USE_I18N = True

AXES_FAILURE_LIMIT = 5
AXES_COOLOFF_TIME = 1
X_FRAME_OPTIONS = "SAMEORIGIN"
TIME_ZONE = "America/Caracas"
USE_I18N = True
USE_TZ = True

# --- Static / media -------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

if DEBUG:
    # Desarrollo: storage simple, sin manifest
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
else:
    # Producción (Vercel serverless): CompressedStaticFilesStorage no necesita manifest
    STORAGES = {
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
    }

# Whitenoise: buscar archivos en runtime vía finders (STATICFILES_DIRS + app dirs)
WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = DEBUG
WHITENOISE_MANIFEST_STRICT = False
WHITENOISE_ALLOW_ALL_ORIGINS = True
WHITENOISE_ROOT = BASE_DIR / "staticfiles"  # directorio post-collectstatic

# --- Tailwind -------------------------------------------------------------
TAILWIND_APP_NAME = "theme"
INTERNAL_IPS = ["127.0.0.1"]



AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

