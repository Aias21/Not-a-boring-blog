from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models.comment import Comment
from ..models.post import Post
from ..models.user import Role
from ..models.views import View
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json
from django.contrib.auth.hashers import make_password
from django.utils.timezone import now
from datetime import timedelta


class CreateRepostRequestTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='user', password='passworduser')
        
        self.blogger = User.objects.create(username='blogger', password=make_password('bloggerpass'))
        self.blogger_role = Role.objects.create(user=self.blogger, is_blogger=True)
        self.blogger_token = Token.objects.create(user=self.blogger)  

        self.blogger2 = User.objects.create(username='blogger2', password=make_password('bloggerpass2'))
        self.blogger_role2 = Role.objects.create(user=self.blogger2, is_blogger=True)
        self.blogger_token2 = Token.objects.create(user=self.blogger2) 

        self.post = Post.objects.create(
            title='Test post Post',
            body='Test post Body',
            user_id=self.blogger,
            status='published',
            min_read='5',
            description='Test post Description'
        )
        self.url = reverse('not_a_boring_blog:request_repost', kwargs={'post_id': self.post.id})

