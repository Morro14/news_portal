from django.forms import ModelForm
from .models import Post, User


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['head', 'type', 'author', 'text', ]


class ProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

