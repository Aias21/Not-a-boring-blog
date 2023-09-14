from django.urls import path, include
from .views.view import record_post_view, get_post_view_count
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
from .views.comment import (
    PostCommentList,
    CreateComment,
    UpdateComment,
    CreateReply,
)


app_name = "not_a_boring_blog"
urlpatterns = [

    # post endpoints
    path('post_list/', PostList.as_view(), name='post-list'),
    path('post_detail/<int:pk>/', PostDetail.as_view(), name='post-detail'),
    path('post_create/', PostCreate.as_view(), name='post-create'),
    path('public_posts/', GetPublicPosts.as_view(), name='get-public-posts'),
    path('user_posts/', OnlyUserPostsView.as_view(), name='only-user-posts'),
    
    #comments
    path('<int:post_id>/comments/', PostCommentList.as_view(), name='comments'),
    path('<int:post_id>/create_comment/', CreateComment.as_view(), name='create_comment'),
    path('<int:comment_id>/create_reply/', CreateReply.as_view(), name='create_reply'),
    path('<int:comment_id>/update_comment/', UpdateComment.as_view(), name='update_comment'),
    # ^ updates or deletes depending on the request method, works with comments as well as replies


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
    path('<int:post_id>/view_count/', get_post_view_count, name='get_post_view_count')
]