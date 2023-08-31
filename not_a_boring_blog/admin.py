from django.contrib import admin
from .models.comment import Comment, ReplyComment
from .models.post import Post, Category
from .models.user import Role


admin.site.register(Comment)
admin.site.register(ReplyComment)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Role)