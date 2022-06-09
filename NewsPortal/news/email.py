from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from .models import User, Post
from datetime import datetime


def get_subscribers(post):
    categories = post.cat.all()
    subscribers = []
    email_list = []

    for c in categories:
        subscribers.append(c.subscribers.values('email'))
    for query in subscribers:
        for e in query:
            email_list.append(e['email'])
    return email_list


def send_weekly_posts():
    time_threshold = datetime.datetime.now() - datetime.timedelta(weeks=1)
    posts = Post.objects.filter(create_time__gt=time_threshold)
    context = {'posts': posts}
    email_subject = "New Posts"
    email_body = render_to_string('email_message.txt', context)
    emails = User.objects.all().values_list('email', flat=True).distinct()
    email = EmailMessage(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, emails)
    print(posts, emails)
    return email.send(fail_silently=False)


def notify_users_newpost(post):
    categories = post.cat.all()
    email = get_subscribers(post)
    link = f'http://127.0.0.1:8000/news/{post.pk}'
    variables = {'post': post, 'link': link, 'categories': categories}
    html_content = render_to_string('email_newpost.html', variables)
    text_content = render_to_string('email_newpost.html', variables)
    msg = EmailMultiAlternatives(
        subject=f'{post.author}{post.create_time.strftime("%d %m %Y")} {post.head}',
        body=text_content,
        from_email='i0ann@yandex.ru',
        to=email,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    



