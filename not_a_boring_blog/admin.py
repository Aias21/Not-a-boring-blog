from django.contrib import admin
from .models.comment import Comment, ReplyComment

# Register your models here.

admin.site.register(Comment)
admin.site.register(ReplyComment)