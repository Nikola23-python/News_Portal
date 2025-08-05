"""
WSGI config for NewsPaper project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper1.settings')

application = get_wsgi_application()

sys.path.append(str(Path(__file__).parent.parent))
