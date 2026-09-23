from pathlib import Path
import os

from dotenv import load_dotenv
from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key


# ============================================================
# LOAD .env FILE (dev convenience — production sets real env vars)
# ============================================================

load_dotenv(BASE_DIR / ".env") if False else None  # placeholder, moved below after BASE_DIR


# ============================================================
# BASE
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env now that BASE_DIR exists
load_dotenv(BASE_DIR / ".env")


# ============================================================
# ENVIRONMENT HELPERS
# ============================================================

def env_bool(name, default=False):
    """Parse boolean env vars strictly. Only these count as True: 1,true,yes,on"""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default=None):
    """Parse comma-separated env var into a list."""
    value = os.environ.get(name)
    if not value:
        return default or []
    return [item.strip() for item in value.split(",") if item.strip()]


DEBUG = env_bool("DJANGO_DEBUG", False)


# ============================================================
# SECRET KEY
# ============================================================

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

if not SECRET_KEY:
    if DEBUG:
        # Dev-only: generate a random key each run.
        # This avoids a hardcoded "django-insecure-..." key ever reaching production.
        SECRET_KEY = get_random_secret_key()
    else:
        raise ImproperlyConfigured(
            "DJANGO_SECRET_KEY environment variable is required when DEBUG=False. "
            "Generate one with: python -c \"from django.core.management.utils "
            "import get_random_secret_key; print(get_random_secret_key())\""
        )


# ============================================================
# ALLOWED HOSTS
# ============================================================

ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
    default=[
        "gitanjalistationary.com",
        "www.gitanjalistationary.com",
    ],
)

if DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", "localhost"]


# ============================================================
# CSRF TRUSTED ORIGINS
# ============================================================

CSRF_TRUSTED_ORIGINS = env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default=[
        "https://gitanjalistationary.com",
        "https://www.gitanjalistationary.com",
    ],
)


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    # --- Third-party security / hardening ---
    "axes",                          # brute-force protection (login rate limiting)
    "csp",                           # Content-Security-Policy headers

    # --- Django built-ins ---
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # --- Local apps ---
    "store",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "csp.middleware.CSPMiddleware",                   # must be first
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "axes.middleware.AxesMiddleware",                 # after AuthenticationMiddleware
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# AUTHENTICATION BACKENDS (required by django-axes)
# ============================================================

AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",            # must be first
    "django.contrib.auth.backends.ModelBackend",
]


# ============================================================
# URL / APPLICATION CONFIG
# ============================================================

ROOT_URLCONF = "gitanjali_site.urls"

WSGI_APPLICATION = "gitanjali_site.wsgi.application"
ASGI_APPLICATION = "gitanjali_site.asgi.application"


# ============================================================
# TEMPLATES
# ============================================================

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
                "store.admin_context_processors.admin_stats",
            ],
        },
    },
]


# ============================================================
# DATABASE
# ============================================================
# SQLite for local development (default).
# PostgreSQL for production — but ONLY if DB_ENGINE=postgres is set.
#
# This means:
#   - You can run `check --deploy` locally with DEBUG=False and SQLite.
#   - Production will use Postgres only when you explicitly configure it.

DB_ENGINE = os.environ.get("DB_ENGINE", "sqlite").lower()

if DB_ENGINE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("DB_NAME", "gitanjali"),
            "USER": os.environ.get("DB_USER", "gitanjali"),
            "PASSWORD": os.environ.get("DB_PASSWORD", ""),
            "HOST": os.environ.get("DB_HOST", "127.0.0.1"),
            "PORT": os.environ.get("DB_PORT", "5432"),
            "CONN_MAX_AGE": 60,
            "OPTIONS": {
                "connect_timeout": 10,
            },
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 10,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# ============================================================
# LANGUAGE / TIME
# ============================================================

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"

USE_I18N = True
USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# DEFAULT PRIMARY KEY
# ============================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# SESSION SECURITY
# ============================================================

SESSION_COOKIE_AGE = 1209600                # 2 weeks
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"


# ============================================================
# CSRF
# ============================================================
# CSRF_COOKIE_HTTPONLY must stay False so JS can read the token
# for AJAX POST requests. This is correct — do NOT change to True.

CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = False
CSRF_COOKIE_SAMESITE = "Lax"


# ============================================================
# DJANGO-AXES  (brute-force / credential-stuffing protection)
# ============================================================

AXES_FAILURE_LIMIT = 5                     # lock after 5 failed attempts
AXES_COOLOFF_TIME = 1                      # lockout duration in hours
AXES_LOCKOUT_PARAMETERS = [["username", "ip_address"]]
AXES_RESET_ON_SUCCESS = True
AXES_ENABLE_ACCESS_FAILURE_LOG = True


# ============================================================
# CONTENT SECURITY POLICY (django-csp)
# ============================================================
# Start strict; loosen only if a legit resource is blocked.

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "img-src": ["'self'", "data:", "https:"],
        "script-src": ["'self'"],
        "style-src": ["'self'", "'unsafe-inline'"],
        "font-src": ["'self'", "data:"],
        "connect-src": ["'self'"],
        "frame-ancestors": ["'none'"],
        "base-uri": ["'self'"],
        "form-action": ["'self'"],
    },
}


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:
    # --- HTTPS enforcement ---
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

    # --- Secure cookies ---
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

    # --- Browser security headers ---
    X_FRAME_OPTIONS = "DENY"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

    # --- HSTS (1 year) ---
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

else:
    # --- Development: keep local HTTP convenient ---
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    X_FRAME_OPTIONS = "DENY"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"


# ============================================================
# LOGGING  (capture auth failures + server errors)
# ============================================================

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "loggers": {
        "django.security": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "axes": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}