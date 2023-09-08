from django.urls import path, include
from .views.views import home
from .views.post import PostList, PostDetail, PostCreate
from .views.user import (
    UserList,
    RegisterUser,
    UpdateUser,
    LoginUser,
    LogoutUser,
    UpdateUserRole,
)

app_name = "not_a_boring_blog"
urlpatterns = [
    path('home/', home, name='home'),
  
    # post endpoints
    path('post_list/', PostList.as_view(), name='post-list'),
    path('post_detail/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('post_create/', PostCreate.as_view(), name='post-create'),
  
    # user endpoints
    path('update_role/<int:id>/', UpdateUserRole.as_view(), name='update_role'),
    path('users_list/', UserList.as_view(), name='users_list'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('update_user/<int:id>/', UpdateUser.as_view(), name='update_user'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]
