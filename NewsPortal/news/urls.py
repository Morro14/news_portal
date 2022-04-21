from django.urls import path
from .views import PostsList, PostDetail, PostSearch, PostDeleteView, PostCreateView, PostUpdateView, CategoryListView
from .views import subscribe_category

urlpatterns = [
    path('', PostsList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('search/', PostSearch.as_view()),
    path('add/', PostCreateView.as_view()),
    path('<int:pk>/edit', PostUpdateView.as_view()),
    path('<int:pk>/delete', PostDeleteView.as_view()),
    path('categories/', CategoryListView.as_view()),
    path('categories/subscribe/', subscribe_category, name='subscribe')
]
