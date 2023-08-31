from django.db import models

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    comment_body = models.TextField()
    following_user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField()    

    def __str__(self):
        return self.comment_body[:50]    

class ReplyComment(models.Model):
    reply_comment_id = models.AutoField(primary_key=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    body = models.TextField()
    following_user = models.ForeignKey('User', on_delete=models.CASCADE)
    created_at = models.DateTimeField()    

    def __str__(self):
        return self.body[:50]
