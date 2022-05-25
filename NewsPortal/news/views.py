from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView, View

from .email import send_weekly_posts
from .models import Post, Category, User
from .filters import PostFilter
from .forms import PostForm, ProfileForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from .tasks import hello, add


class PostsList(ListView):
    model = Post
    ordering = 'create_time'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'post_search'
    ordering = ['-create_time']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class PostCreateView(CreateView, PermissionRequiredMixin):
    template_name = 'post_create.html'
    form_class = PostForm
    context_object_name = 'post_create'
    success_url = '/news/'
    permission_required = ('news.add_post',)


class PostUpdateView(UpdateView, PermissionRequiredMixin):
    template_name = 'post_create.html'
    form_class = PostForm
    context_object_name = 'post_update'
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'post_delete'


class ProfileEdit(UpdateView, LoginRequiredMixin):
    template_name = 'profile_edit.html'
    form_class = ProfileForm


class CategoryListView(ListView):
    model = Category
    template_name = "category_list.html"
    context_object_name = "categories"
    ordering = 'name'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_sub'] = self.request.user.category_set.all()

        return context


@login_required
def subscribe_category(request, category):
    user_ = request.user

    category_ = Category.objects.get(name=f"{category}")
    if not request.user.category_set.filter(name=f"{category_}").exists():
        category_.subscribers.add(user_)

    return redirect('/news/categories')



        

