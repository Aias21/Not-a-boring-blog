from django.urls import path, include
from .views.views import home
from .views.post import PostList, PostDetail, PostCreate


app_name = "not_a_boring_blog"
urlpatterns = [
    path('home/', home, name='home'),
    path('post_list/', PostList.as_view(), name='post-list'),
    path('post_detail/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('post_create/', PostCreate.as_view(), name='post-create'),
    ]