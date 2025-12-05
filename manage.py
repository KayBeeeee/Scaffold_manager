#!/usr/bin/env python
import os
import sys


def main():
    # Detect Azure → use production settings
    use_prod = False

    # Azure environment variables
    azure_vars = ["WEBSITE_INSTANCE_ID", "WEBSITE_SITE_NAME", "AZURE_DEPLOYMENT"]

    for var in azure_vars:
        if os.environ.get(var):
            use_prod = True
            break

    if use_prod:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.prod")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
