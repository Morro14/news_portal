import datetime
from celery import shared_task

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from celery.utils.log import get_task_logger
from .models import Post, User
from .email import send_weekly_posts, notify_users_newpost


logger = get_task_logger(__name__)


@shared_task(name="new_post_mail_task")
def new_post_mail_task(post):
    notify_users_newpost(post)


@shared_task(name="weekly_posts_mail_task")
def weekly_mail(posts):
    logger.info("Send weekly posts")
    return send_weekly_posts()


@shared_task(name='test')
def test():
    print("Test")


