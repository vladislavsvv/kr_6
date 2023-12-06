from datetime import datetime

from django.core.cache import cache
from django.core.mail import send_mail

from blog.models import Blog
from config import settings
from config.settings import CACHE_ENABLED
from mailing.models import Mailing, Logs


def send_order_email(obj: Mailing):
    try:
        send_mail(
            subject=obj.title_message,
            message=obj.body_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[*obj.client.all()],
            fail_silently=True)

        logs = Logs.objects.create(
            mailing=obj,
            datetime_of_last_attempt=datetime.now(),
            status=True,
            error_msg='200 OK'

        )
    except Exception as e:

        logs = Logs.objects.create(
            mailing=obj,
            datetime_of_last_attempt=datetime.now(),
            status=False,
            error_msg=str(e)

        )


def time_task():
    current_date = datetime.now().date()

    mailings_created = Mailing.objects.filter(status='created')

    if mailings_created.exists():

        for mailing in mailings_created:
            if mailing.start_time <= current_date <= mailing.end_time:

                mailing.status = 'started'
                mailing.save()

    mailings_launched = Mailing.objects.filter(status='started')

    if mailings_launched.exists():

        for mailing in mailings_launched:

            if mailing.start_time <= current_date <= mailing.end_time:
                if mailing.last_run:
                    differance = current_date - mailing.last_run
                    if mailing.period == 'daily':
                        if differance.days == 1:
                            send_order_email(mailing)
                            mailing.last_run = current_date
                            mailing.save()
                    elif mailing.period == 'weekly':
                        if differance.days == 7:
                            send_order_email(mailing)
                            mailing.last_run = current_date
                            mailing.save()
                    elif mailing.period == 'monthly':
                        if differance.days == 30:
                            send_order_email(mailing)
                            mailing.last_run = current_date
                            mailing.save()
                else:
                    send_order_email(mailing)
                    mailing.last_run = current_date
                    mailing.save()
            elif current_date >= mailing.end_time:
                mailing.status = 'done'
                mailing.save()


def cache_blog():
    if CACHE_ENABLED:
        key = f'blog_list'
        blog_list = cache.get(key)
        if blog_list is None:
            blog_list = Blog.objects.all()
            cache.set(key, blog_list)
    else:
        blog_list = Blog.objects.all()
    return blog_list
