from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


#   class Profile(models.Model):
#       user = models.OneToOneField(User, on_delete=models.CASCADE)
#       subscriptions = models.ManyToManyField("Category", through="CategoryUser", default=None)


class Category(models.Model):
    def __str__(self):
        return f'{self.name[:124:]}'
    name = models.CharField(unique=True, max_length=255)
    subscribers = models.ManyToManyField(User)



#  class CategoryUser(models.Model):
#      category = models.ForeignKey(Category, on_delete=models.CASCADE)
#      user = models.ForeignKey(User, on_delete=models.CASCADE)


class Post(models.Model):
    def __str__(self):
        return f'{self.head[:124:]} {self.create_time}'
    news = "NW"
    article = "AR"

    TYPES = [(news, 'News'), (article, "Article")]

    type = models.CharField(max_length=2, choices=TYPES, default=news)
    head = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.FloatField(default=0.0)
    create_time = models.DateTimeField(auto_now_add=True, auto_created=True)

    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)


    def like(self, num):
        self.rating += 1.0 * num
        self.save()

    def dislike(self, num):
        self.rating -= 1.0 * num
        self.save()

    def preview(self):
        return self.text[:124:] + "..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True, auto_created=True)
    rating = models.FloatField(default=0.0)

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self, num):
        self.rating += 1.0 * num
        self.save()

    def dislike(self, num):
        self.rating -= 1.0 * num
        self.save()


class Author(models.Model):
    def __str__(self):
        return f'{self.user.username}'
    rating = models.FloatField(default=0.0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def update_rating(self):
        post_rating = Post.objects.filter(author=self).aggregate(Sum('rating'))
        comment_rating = self.user.comment_set.all().aggregate(Sum('rating'))
        author_rating = Comment.objects.filter(user=self.user).aggregate(Sum('rating'))
        self.rating = float(post_rating['rating__sum']) * 3 + float(comment_rating['rating__sum']) + float(author_rating['rating__sum'])
        self.save()
        return self.rating
