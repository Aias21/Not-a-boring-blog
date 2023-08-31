from django.contrib import admin
from .models.comment import Comment, ReplyComment
from .models.post import Post, Category

admin.site.register(Comment)
admin.site.register(ReplyComment)
admin.site.register(Post)
admin.site.register(Category)