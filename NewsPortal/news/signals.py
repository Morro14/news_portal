from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save, post_delete, post_init
from django.dispatch import receiver
from django.template.loader import render_to_string
from datetime import datetime

from .models import Post, User


@receiver(post_save, sender=Post)
def notify_users_newpost(sender, instance, created, **kwargs):
    categories = instance.category.all()
    subscribers = []
    email = []

    for c in categories:
        subscribers.append(c.subscribers.values('email'))
    for query in subscribers:
        for e in query:
            email.append(e['email'])

    link = f'http://127.0.0.1:8000/news/{instance.pk}'
    variables = {'post': instance, 'link': link, 'categories': categories}
    html_content = render_to_string('email_newpost.html', variables)
    text_content = render_to_string('email_newpost.html', variables)

    msg = EmailMultiAlternatives(
        subject=f'{instance.author}{instance.create_time.strftime("%d %m %Y")} {instance.head}',
        body=text_content,
        from_email='i0ann@yandex.ru',
        to=email,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@receiver(post_delete, sender=Post)
def notify_user_delete(sender, instance, created, **kwargs):
    variables = {'post': instance,}
    html_content = render_to_string('email_deletepost.html', variables)
    text_content = render_to_string('email_deletepost.html', variables)
    email = instance.author.user.email
    msg = EmailMultiAlternatives(
       subject=f'Ваш пост был удалён',
       body=text_content,
       from_email='i0ann@yandex.ru',
       to=[email],
    )

    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=User)
def notify_new_user(sender, instance, created, **kwargs):
    if created:
        variables = {'user': instance,}
        html_content = render_to_string('email_welcome.html', variables)
        text_content = render_to_string('email_welcome.html', variables)
        email = instance.email
        msg = EmailMultiAlternatives(
           subject=f'Welcome',
           body=text_content,
           from_email='i0ann@yandex.ru',
           to=[email],
        )

        msg.attach_alternative(html_content, "text/html")
        msg.send()

    pass




