import datetime
from celery import Celery as app, shared_task, schedules, beat
from celery.schedules import crontab
from django.core.mail import EmailMultiAlternatives, send_mass_mail
from django.template.loader import render_to_string
from celery.utils.log import get_task_logger
from .models import Post, User
from .email import send_weekly_posts
import time

logger = get_task_logger(__name__)


@shared_task
def new_post_mail():
    pass


@shared_task(name="send_weekly_posts_task")
def weekly_mail(posts):
    logger.info("Sent weekly posts")
    return send_weekly_posts()

#   app.conf.beat_schedule = {
#       'action_every_week': {
#           'task': 'tasks.send_weekly_posts_task',
#           'schedule': crontab(),
#       },
#   }

def send_mails():
    time_threshold = datetime.datetime.now() - datetime.timedelta(weeks=1)
    new_posts = Post.objects.filter(create_time__gt=time_threshold)
    cat = new_posts.values_list('category')
    subscribers = User.objects.filter(category__in=cat)
    emails = subscribers.values_list('email').distinct()
    email_cat_dict = {}
    for e in emails:
        email_cat_dict.update({e[0]: list(User.objects.get(email=e[0]).category_set.all())})
    emails_list = list(email_cat_dict.keys())

    variables = {'new_posts': new_posts, }
    html_content = render_to_string('email_weekly.html', variables)
    text_content = render_to_string('email_weekly.html', variables)
    msg = EmailMultiAlternatives(
        subject=f'Новые статьи для Вас',
        body=text_content,
        from_email='i0ann@yandex.ru',
        to=emails_list,
    )

    msg.attach_alternative(html_content, "text/html")
    #    msg.content_subtype = "html"
    msg.send()




