from django.urls import path
from .views.views import home
from .views.user import (
    UserList,
    RegisterUser,
    UpdateUser,
    LoginUser,
    LogoutUser,
)

app_name = "not_a_boring_blog"
urlpatterns = [
    path('home/', home, name='home'),
    path('users_list/', UserList.as_view(), name='users_list'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('update_user/<int:id>/', UpdateUser.as_view(), name='update_user'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUser.as_view(), name='logout'),
]