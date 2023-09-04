from django.urls import path
from .views.views import home
from .views.list_post_view import PostListCreateView, PostDetailView


app_name = "not_a_boring_blog"
urlpatterns = [
    path('home/', home, name='home'),
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    ]