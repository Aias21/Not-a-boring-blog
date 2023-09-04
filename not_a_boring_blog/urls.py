from django.urls import path, include
from .views.views import home
from .views.list_post_view import PostListCreateView, PostDetailView, ArticleListView


app_name = "not_a_boring_blog"
urlpatterns = [
    path('home/', home, name='home'),
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    #path('articles/', article_list, name='article-list'),
    #path('articles/', include('not_a_boring_blog.urls')),
    path('articles/', ArticleListView.as_view(), name='article-list'),

    ]