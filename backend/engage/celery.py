import os

from celery import Celery
from django.conf import settings
from django.core.cache import cache
# set the default Django settings module for the 'celery' program.

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'engage.settings.dev')

# app = Celery('erp')
app = Celery('engage')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
app.conf.broker_url = settings.BROKER_URL
app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'
app.conf.broker_transport_options = {'visibility_timeout': 36000}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


def block_multiple_celery_task_execution(task, prefix):
    # prefix actully is not necessary but I thing it's good practice to seperate id of each task 
    # m_cache = caches.all()[0]
    is_task_executed = cache.get(f"{prefix}") # _{task.request.id}
    # print("m_cache", m_cache, "cache", cache)
    # print(f"denied running: {is_task_executed}")
    if not is_task_executed:
        cache.set(f"{prefix}", True, timeout=30) # 30 secs  # _{task.request.id}
        # print(f'cache.get(f"{prefix}")', cache.get(f"{prefix}"))
        # print(f"{prefix}_{task.request.id}", "set to", True)
        # print(f"{prefix}_{task.request.id} set to", cache.get(f"{prefix}_{task.request.id}"))
        return False
    
    print("task has been blocked to prevent multiple execution!")
    return True