from django.urls import path
from .views.view import record_post_view
from .views.post import (
    PostList, 
    PostDetail, 
    PostCreate, 
    GetPublicPosts, 
    OnlyUserPostsView)
from .views.user import (
    UserList,
    RegisterUser,
    UpdateUser,
    LoginUser,
    LogoutUser,
    UpdateUserRole,
    change_password
)

app_name = "not_a_boring_blog"
urlpatterns = [

    # post endpoints
    path('post_list/', PostList.as_view(), name='post-list'),
    path('post_detail/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('post_create/', PostCreate.as_view(), name='post-create'),
    path('public_posts/', GetPublicPosts.as_view(), name='get-public-posts'),
    path('user_posts/', OnlyUserPostsView.as_view(), name='only-user-posts'),
    

    # user endpoints
    path('change_password/', change_password, name='change_password'),
    path('update_role/<int:id>/', UpdateUserRole.as_view(), name='update_role'),
    path('users_list/', UserList.as_view(), name='users_list'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('update_user/<int:id>/', UpdateUser.as_view(), name='update_user'), 
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),

    # post views
    path('record_post_view/<int:post_id>/', record_post_view, name='record_post_view'),
]