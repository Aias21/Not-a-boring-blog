from django.db import models
from .post import Post
from .user import Role


class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_id')
    body = models.CharField(max_length=500)
    user_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.body[:50]    


class ReplyComment(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_id')
    body = models.CharField(max_length=500)
    user_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)     

    def __str__(self):
        return self.body[:50]
