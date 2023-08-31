from django.db import models
from .post import Post
from .user import User

class Comment(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    following_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.body[:50]    

class ReplyComment(models.Model):
    comment_id = models.ForeignKey(Comment, on_delete=models.CASCADE)
    body = models.CharField(max_length=500)
    following_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)     

    def __str__(self):
        return self.body[:50]
