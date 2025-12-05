from .base import *
import os

DEBUG = False

# Fetch from environment
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-prod-secret-key")

# Minimal ALLOWED_HOSTS: set via environment
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")

# Security settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# WhiteNoise for static files
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
