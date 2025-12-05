# config/wsgi.py
import os

# Auto-switch to prod on Azure if flag is enabled or AZURE env detected
azure_detect = any(
    os.environ.get(k) for k in ("WEBSITE_INSTANCE_ID", "WEBSITE_SITE_NAME", "AZURE_DEPLOYMENT")
)


if azure_detect:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
