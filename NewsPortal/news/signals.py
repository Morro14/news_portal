from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import Post


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

    html_content = render_to_string('post.html', {'post': instance})

    msg = EmailMultiAlternatives(
        subject=f'{instance.author}{instance.create_time.strftime("%d %m %Y")}',
        from_email='i0ann@yandex.ru',
        to=email
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()

