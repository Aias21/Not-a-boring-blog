from django.db import models
from .user import Role
from .post import Post


STATUS = (
    ('requested', 'Requested'),
    ('approve', 'Approved'),
    ('denied', 'Denied'),
)


class RepostRequest(models.Model):
    requester_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.CharField(max_length=9, choices=STATUS)