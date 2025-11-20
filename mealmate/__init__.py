"""
ASGI config for mealmate project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mealmate.settings')

application = get_asgi_application()
