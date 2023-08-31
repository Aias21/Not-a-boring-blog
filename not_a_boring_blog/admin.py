from django.contrib import admin
from .models.post_category import Post, Category

# Register your models here.

admin.site.register(Post)
admin.site.register(Category)