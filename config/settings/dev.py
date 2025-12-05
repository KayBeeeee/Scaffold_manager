from .base import *

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-for-local")
ALLOWED_HOSTS = []  # local dev, I will keep this empty
