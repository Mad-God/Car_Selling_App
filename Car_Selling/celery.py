from __future__ import absolute_import, unicode_literals
import os

from celery import  Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "Car_Selling.settings")

app = Celery("Car_Selling")
app.conf.enable_utc = False

app.conf.update(timezone = "Asia/Kolkata")


app.config_from_object(settings, namespace = "CELERY")


# CELERY BEAT SETINGS
app.conf.beat_schedule = {
    "daily-promotional-mails":{
        "task":"sales.tasks.send_promoitonal_mails", 
        "schedule":crontab(hour=16,minute=56), # works in 24 hour format, i.e, 8=8am, 20=8pm
        # use "args":(arg1, arrg2...) to pass additional args to the task_func
    }
}



app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")

