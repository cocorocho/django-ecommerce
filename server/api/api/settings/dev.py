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

FRONTEND_URL = "http://localhost:3000"

# CORS
CORS_ALLOWED_ORIGINS = [FRONTEND_URL]

# Email
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "mail"

DJOSER["PASSWORD_RESET_CONFIRM_URL"] = FRONTEND_URL + "/" + "account/recover/{uid}/{token}/"
