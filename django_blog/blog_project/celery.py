# monblog/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monblog.settings')

app = Celery('blog_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
