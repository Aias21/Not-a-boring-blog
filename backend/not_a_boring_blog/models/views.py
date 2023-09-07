from django.db import models
from .user import Role
from .post import Post

class View(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)