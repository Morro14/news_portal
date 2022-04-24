import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, User


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



#    link = f'http://127.0.0.1:8000/news/{instance.pk}'
    variables = {'new_posts': new_posts, }
    html_content = render_to_string('email_weekly.html', variables)
    text_content = render_to_string('email_weekly.html', variables)
    msg = EmailMultiAlternatives(
       subject=f'Новые статьи для Вас',
       body=text_content,
       from_email='i0ann@yandex.ru',
       to=emails_list,
    )

#    msg.attach_alternative(html_content, "text/html")
    msg.content_subtype = "html"
    msg.send()


