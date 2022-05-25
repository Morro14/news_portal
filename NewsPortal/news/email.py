from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from .models import User, Post
from datetime import datetime

def send_weekly_posts():
    time_threshold = datetime.datetime.now() - datetime.timedelta(weeks=1)
    posts = Post.objects.filter(create_time__gt=time_threshold)
    context = {'posts': posts}
    email_subject = "New Posts"
    email_body = render_to_string('email_message.txt', context)
    emails = User.objects.all().values_list('email', flat=True).distinct()
    print(posts)
    email = EmailMessage(email_subject, email_body, settings.DEFAULT_FROM_EMAIL, emails)

    return email.send(fail_silently=False)



