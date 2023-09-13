from django.db import models
from .post import Post
from django.contrib.auth import get_user_model


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    body = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='reply')

    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return str(self.pk)

    @property
    def children(self):
        return Comment.objects.filter(parent_id=self).reverse()

    @property
    def is_parent(self):
        if self.parent_id is None:
          return True
        return False

# class ReplyComment(models.Model):
#     comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_id')
#     body = models.CharField(max_length=500)
#     user_id = models.ForeignKey(Role, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.body[:50]
