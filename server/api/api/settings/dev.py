from .base import *

INSTALLED_APPS += [
    "debug_toolbar"
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware"
]

# Debug Toolbar
INTERNAL_IPS = (
    "localhost",
    "127.0.0.1"
)

# CORS
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]

# Email
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "mail"