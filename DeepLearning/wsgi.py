"""
WSGI config for DeepLearning project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

# wsgi.py
import sys
import os

# 添加 DeepLearning 目录到 Python 路径中
sys.path.append(os.path.join(os.path.dirname(__file__), '..\\DeepLearning'))

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
