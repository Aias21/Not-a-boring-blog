from django.urls import path
from .views.views import home
from .views.user import UserList, RegisterUser, UpdateUser, LoginUser

app_name = "not_a_boring_blog"
urlpatterns = [
    path('home/', home, name='home'),
    path('users_list/', UserList.as_view(), name='users_list'),
    path('register_user/', RegisterUser.as_view(), name='register_user'),
    path('update_user/<int:id>/', UpdateUser.as_view(), name='update_user'),
    path('login_user/', LoginUser.as_view(), name='login_user'),
]