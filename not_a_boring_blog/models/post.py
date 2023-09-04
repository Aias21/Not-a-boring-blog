# The above code defines two Django models, Category and Post, with various fields and relationships.
from django.db import models
from .user import Role


class Category(models.Model):
    category_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category_name


class Post(models.Model):
    STATUS = [
        ('published', 'Published'),
        ('private', 'Private'),
        ('editing', 'Editing'),
    ]
    category = models.ManyToManyField(Category) # on_delete=models.CASCADE is not applied in ManyToMany
    title = models.CharField(max_length=255)
    body = models.TextField()
    user_id = models.ForeignKey(Role, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS)
    created_at = models.DateTimeField(auto_now_add=True) # the field will be automatically set to the current timestamp when a new object is created. It will not change when the object is updated in the future.
    last_updated = models.DateTimeField(auto_now=True) # the field will be automatically updated to the current timestamp every time the object is saved (updated), regardless of whether it's a new object or an existing one
    min_read = models.CharField(max_length=50)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title
