from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_moderator = models.BooleanField(default=False)
    is_blogger = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    bio = models.CharField(max_length=500)
    # created_at is by default defined in User model - will be updated later with serializer
    # last_login is by default defined in User model - will be updated later with serializer
    # email is by default defined in User model - will be updated later with serializer

    def __str__(self):
        return self.user.username
