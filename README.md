Scaffold Manager

Scaffold Manager is a Django-based asset management system built to track scaffold components across sites. It includes full CRUD functionality, filtering, pagination, CSV export, and automatic production configuration when deployed on Azure App Service.

Features
• Full CRUD operations for scaffold components
• Search, filtering, and pagination
• Summary counts by site and condition
• Custom ordering (NEW → GOOD → REPAIR → SCRAP → name)
• Toggle “In Use” directly from the asset detail page
• CSV export of the currently filtered asset list
• Automatic production vs development settings switching using environment variables
• Azure-ready static files setup using WhiteNoise

Optional Feature Implemented: CSV Export
The system allows exporting the currently filtered asset list to CSV. A new route was added:
/assets/export/csv/
It exports only the items that match the filters currently applied on-screen.

Deployment (Azure App Service)
The project automatically switches to production settings when running on Azure. This is achieved through multiple settings modules:
config/settings/base.py
config/settings/dev.py
config/settings/prod.py
Local development uses dev.py. Azure automatically uses prod.py when the environment variable AZURE_DEPLOYMENT=1 is present.

How Auto-Switch Works
Inside Azure, under App Service → Configuration, when the variable:
AZURE_DEPLOYMENT = 1
is present, Azure’s gunicorn startup command loads:
config.settings.prod
This activates:
- DEBUG=False
- Secure cookies
- WhiteNoise static file serving
- Environment-based SECRET_KEY and ALLOWED_HOSTS

Required Environment Variables on Azure
Set these in Azure → App Service → Configuration → Application Settings:
AZURE_DEPLOYMENT = 1
SECRET_KEY = Your Django secret key
ALLOWED_HOSTS = scaffold-asset-manager-xxxx.azurewebsites.net

Optional Variables
DATABASE_URL
ALLOWED_HOSTS (multiple comma separated)


Local Development Setup
python -m venv venv
venv\Scripts\activate (Windows)
source venv/bin/activate (Mac/Linux)
pip install Django
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
Open http://127.0.0.1:8000/assets/

Application Overview
List View: search, filter, pagination, CSV export
Detail View: full asset info, toggle in_use
Create/Edit Views: validation, unique constraints
Delete View: confirmation

Tests
Covers validation, CRUD, pagination, filtering, toggle.

GitHub Repo:
https://github.com/KayBeeeee/Scaffold_manager
