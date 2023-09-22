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
