import os
from django.core.asgi import get_asgi_application

use_prod = False
azure_vars = ["WEBSITE_INSTANCE_ID", "WEBSITE_SITE_NAME", "AZURE_DEPLOYMENT"]

for var in azure_vars:
    if os.environ.get(var):
        use_prod = True
        break

if use_prod:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

application = get_asgi_application()
