from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255)


class Post(models.Model):
    news = "NW"
    article = "AR"

    TYPES = [(news, 'News'), (article, "Article")]

    type = models.CharField(max_length=2, choices=TYPES, default=news)
    head = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.FloatField(default=0.0)
    create_time = models.DateTimeField(auto_created=True)

    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, through="PostCategory", default=None)

    def like(self, num):
        self.rating += 1.0 * num

    def dislike(self, num):
        self.rating -= 1.0 * num

    def preview(self):
        return self.text[:124:] + "..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    create_time = models.DateTimeField(auto_created=True)
    rating = models.FloatField(default=0.0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self, num):
        self.rating += 1.0 * num

    def dislike(self, num):
        self.rating -= 1.0 * num


class Author(models.Model):
    rating = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))
        comment_rating = self.user.comment_set.all().aggregate(Sum('rating'))
        author_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))

        return post_rating * 3 + comment_rating + author_rating


