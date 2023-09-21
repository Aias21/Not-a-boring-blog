from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from ...models.post import Category, Post
from django.contrib.auth.models import User
from ...serializers.posts import PostSerializer
from ...permissions import IsAdminRole, IsModeratorRole
from django.urls import reverse

class TestPostListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='testuser', password='testpassword')
        self.admin = User.objects.create(username='adminuser', password='adminpassword')
        self.moderator = User.objects.create(username='moderatoruser', password='moderatorpassword')
        self.category = Category.objects.create(category_name='Test Category')
        self.post = Post.objects.create(
            title='Test Post',
            body='Test Body',
            user_id=self.user,
            status='published',
            min_read='5 mins',
            description='Test Description',
        )
        self.post.category.add(self.category)

def test_list_posts(self):
    url = reverse('post_list')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)

    expected_data = PostSerializer(instance=[self.post], many=True).data
    self.assertEqual(response.data, expected_data)




