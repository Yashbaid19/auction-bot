"""
ASGI config for auction_bot project (simplified - no WebSockets).
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_bot.settings')

application = get_asgi_application()

