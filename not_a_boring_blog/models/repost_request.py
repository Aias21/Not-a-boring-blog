from django.db import models
from .user import Role
from .post import Post
from django.contrib.auth.models import User

STATUS = (
    ('requested', 'Requested'),
    ('approved', 'Approved'),
    ('denied', 'Denied'),
)


class RepostRequest(models.Model):
    requester_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='repost')
    status = models.CharField(max_length=9, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-status', 'created_at']

