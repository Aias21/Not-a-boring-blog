from django.db import models
from .user import Role
from .post import Post
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions
from datetime import datetime, timedelta



COOLDOWN_PERIOD = timedelta(minutes=5)


class View(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)