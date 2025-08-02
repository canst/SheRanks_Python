# C:\Users\soyam\Documents\GitHub\SheRanks_Python\api\index.py

import os
import django
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sheranks_project.settings')
django.setup()

application = get_wsgi_application()

# Vercel's handler is often named 'handler' or 'app'
# We will explicitly map our Django application to it
def handler(request, event):
    return application(request, event)