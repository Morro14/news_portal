from django.urls import path
from .views import PostsList, PostDetail, PostSearch, PostDeleteView, PostCreateView, PostUpdateView, CategoryListView
from .views import subscribe_category
from django.views.decorators.cache import cache_page

urlpatterns = [
#    path('test/', IndexView.as_view()),
    path('', cache_page(60)(PostsList.as_view()), name='posts_list'),
    path('<int:pk>/', cache_page(300)(PostDetail.as_view()), name='post_detail'),
    path('search/', PostSearch.as_view()),
    path('add/', PostCreateView.as_view()),
    path('<int:pk>/edit', PostUpdateView.as_view()),
    path('<int:pk>/delete', PostDeleteView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('categories/subscribe/<str:category>', subscribe_category, name='subscribe'),
]
