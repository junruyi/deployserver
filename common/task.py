from __future__ import absolute_import

from django.core.mail import send_mail
from django.conf  import settings
from common import celery_app as app


@app.task
def send_mail_async(*args, **kwargs):
    if len(args) == 3:
        args = list(args)
        args[0] = settings.EMAIL_SUBJECT_PREFIX + args[0]
        args.insert(2, settings.EMAIL_HOST_USER)
        args = tuple(args)

    send_mail(*args, **kwargs)