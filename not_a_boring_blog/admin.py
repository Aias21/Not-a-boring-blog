from django.contrib import admin

# Register your models here.
from .models.post_category import Post, Category

admin.site.register(Post)
admin.site.register(Category)