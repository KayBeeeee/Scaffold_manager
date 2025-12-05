from .base import *
import os

DEBUG = True

# Fetching from environment
SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-prod-secret-key")


ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "*").split(",")


SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Trusted origins for CSRF 
CSRF_TRUSTED_ORIGINS = [
    "https://scaffold-asset-manager-gtbcbaakhjd0b4c2.southafricanorth-01.azurewebsites.net"
]

# WhiteNoise settings for static files
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
