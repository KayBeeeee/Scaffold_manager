from .base import *
import os

DEBUG = False

# Use environment variable or fallback
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# Security for cookies if HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Insert WhiteNoise middleware near the top (after SecurityMiddleware)
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# WhiteNoise static files storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
