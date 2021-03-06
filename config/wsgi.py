"""
WSGI config for homeinventory project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

from whitenoise import WhiteNoise
from django.conf import settings

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")

# This allows easy placement of apps within the interior
# homeinventory directory.
app_path = os.path.dirname(os.path.abspath(__file__)).replace('/config', '')
sys.path.append(os.path.join(app_path, 'homeinventory'))

application = get_wsgi_application()

application = WhiteNoise(application,
                         root=settings.STATIC_ROOT,
                         prefix=settings.STATIC_URL)
