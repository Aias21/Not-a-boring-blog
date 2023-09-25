from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models.comment import Comment
from ..models.post import Post
from ..models.user import Role
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token



class PostCommentListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='user', password='passworduser')
        
        self.blogger = User.objects.create(username='blogger', password='blogger')
        self.blogger_role = Role.objects.create(user=self.blogger, is_blogger=True)
        self.blogger_token = Token.objects.create(user=self.blogger)
        
        self.blogger2 = User.objects.create(username='blogger2', password='blogger2')
        self.blogger_role2 = Role.objects.create(user=self.blogger2, is_blogger=True)
        self.blogger_token2 = Token.objects.create(user=self.blogger2)
        
        self.post = Post.objects.create(
            title='Sample Post',
            body='Sample Body',
            user_id=self.blogger,
            status='published',
            min_read='5 mins',
            description='Sample Description'
        )     

        self.url = reverse('not_a_boring_blog:comments', kwargs={'post_id': self.post.id})


    def test_list_comments_unauthorized(self):
        self.comment1 = Comment.objects.create(post_id=self.post, author=self.blogger, body='Comment 1')
        self.comment2 = Comment.objects.create(post_id=self.post, author=self.blogger, body='Comment 2')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_list_comments_authorized(self):
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.blogger_token.key}',
            'content_type': 'application/json',
        }
        self.comment1 = Comment.objects.create(post_id=self.post, author=self.blogger, body='Comment 3')
        self.comment2 = Comment.objects.create(post_id=self.post, author=self.blogger, body='Comment 4')
        response = self.client.get(self.url, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_list_comments_no_comments(self):
        Comment.objects.filter(post_id_id=self.post.id).delete()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_list_comments_no_comments(self):
    #     comments_before_delete = Comment.objects.filter(post_id_id=self.post.id).count()
    #     Comment.objects.filter(post_id_id=self.post.id).delete()

    #     comments_after_delete = Comment.objects.filter(post_id_id=self.post.id).count()

    #     response = self.client.get(self.url)
        
    #     print("Number of comments before delete:", comments_before_delete)
    #     print("Number of comments after delete:", comments_after_delete)
        
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
