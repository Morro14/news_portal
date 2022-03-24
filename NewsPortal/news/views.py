from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from news.models import *

User.objects.create_user('Bob')
User.objects.create_user('Alex')

user_1 = User.objects.get(id=5)
user_2 = User.objects.get(id=6)

Author.objects.create(user=user_1)
Author.objects.create(user=user_2)

author_1 = Author.objects.get(id=1)
author_2 = Author.objects.get(id=2)

Category.objects.create(name='Technology')
Category.objects.create(name='Business')
Category.objects.create(name='Sports')
Category.objects.create(name='Science')

technology = Category.objects.get(id=1)
business = Category.objects.get(id=2)
sports = Category.objects.get(id=3)
science = Category.objects.get(id=4)

Post.objects.create(
    type='AR',
    head="James Webb Space Telescope takes highest resolution infrared image",
    text="The James Webb Space Telescope (JWST) has reached a crucial phase in the alignment of its mirrors. Images "
         "from this process have shown that everything is working even better than expected, and the telescope’s "
         "operators say that its performance will be able to meet or even exceed the goals that were originally set "
         "for it. ",
    author=author_1
)
Post.objects.create(
    type='AR',
    head="Will Russia default on its foreign debt for first time in more than 100 years?",
    text="""Russia faces a payment deadline for two international bonds today – worth $117 million – but it's unclear
    whether Moscow will be able to pay. The finance ministry has said its ability to make foreign payments has been
    hampered by sanctions. If Russia is unable to make the payments within a 30-day grace period, it will face its
    first default on international debt in more than a century. Also today, two fuel depots in western France have
    been blockaded in protest at high prices. """,
    author=author_2
)
Post.objects.create(
    type='NW',
    head="Chelsea restrictions: Fans now able to buy certain match tickets after government licence amended",
    text="Chelsea are operating under a special government licence after the UK sanctioned owner Roman Abramovich; "
         "Fans can purchase tickets for away matches, cup games and women's fixtures, but not for home Premier League "
         "games",
    author=author_1
)

article_1 = Post.objects.get(id=1)
article_2 = Post.objects.get(id=2)
news_1 = Post.objects.get(id=3)

article_1.category.add(technology, science)
article_2.category.add(business)
news_1.category.add(sports)

Comment.objects.create(text='Interesting take', post=article_1, user=user_1)
Comment.objects.create(text='Продам гараж', post=article_2, user=user_1)
Comment.objects.create(text='Bullshit', post=news_1, user=user_2)
Comment.objects.create(text='I disagree', post=news_1, user=user_2)

comment_1 = Comment.objects.get(id=1)
comment_2 = Comment.objects.get(id=2)
comment_3 = Comment.objects.get(id=3)
comment_4 = Comment.objects.get(id=4)

article_1.like(33)
article_2.like(115)
article_2.dislike(70)
news_1.dislike(285)

comment_1.like(15)
comment_2.like(63)
comment_2.dislike(5)
comment_3.like(55)
comment_3.dislike(109)
comment_4.like(44)

author_1.update_rating()
author_2.update_rating()

best_user = Author.objects.all().order_by('-rating')[0].user
print(f'Пользователь с наивысшим рейтингом: {best_user.username}')

best_post = Post.objects.all().order_by('-rating')[0]
Post.objects.all().order_by('-rating').values('create_time', 'author__user__username', 'rating','text')[0]
print(best_post.preview())

best_comment = best_post.comment_set.order_by('-rating')[0]
best_comment.user.username
best_comment.rating
best_comment.text
