from django.urls import path
from .views.views import home

app_name = "not_a_booring_blog"
urlpatterns =[
    path('home/', home, name='home')
]