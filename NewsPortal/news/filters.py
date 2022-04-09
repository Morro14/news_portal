from django_filters import FilterSet, DateFilter
from .models import Post
import django.forms


class PostFilter(FilterSet):
    create_time = DateFilter(lookup_expr='gt', widget=django.forms.DateInput(attrs={'type': 'date'})
                         )
    class Meta:
        model = Post
        fields = {
            'head': ['icontains'],
            'author__user__username': ['icontains'],
            'type': ['icontains']
        }

