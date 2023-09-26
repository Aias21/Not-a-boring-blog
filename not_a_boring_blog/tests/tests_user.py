from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from ..models.comment import Comment
from ..models.post import Post
from ..models.user import Role
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
import json
from django.contrib.auth.hashers import make_password


class ChangeUserPasswordTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='user', password='passworduser')
        
        self.blogger = User.objects.create(username='blogger', password=make_password('bloggerpass'))
        self.blogger_role = Role.objects.create(user=self.blogger, is_blogger=True)
        self.blogger_token = Token.objects.create(user=self.blogger)  

        self.url = reverse('not_a_boring_blog:change_password')


    def test_change_password_by_blogger(self):
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.blogger_token.key}',
            'content_type': 'application/json',
        }
        data = {
            'current_password': 'bloggerpass',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123',
        }
        response = self.client.put(self.url, data=json.dumps(data), **headers)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_change_password_by_unregistered_user(self):
        data = {
            'current_password': 'passworduser',
            'new_password': 'newpassword1234',
            'confirm_password': 'newpassword1234',
        }
        response = self.client.put(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_change_password_incorrect_current_password(self):
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.blogger_token.key}',
            'content_type': 'application/json',
        }
        data = {
            'current_password': 'incorrectpassword',
            'new_password': 'newpassword123',
            'confirm_password': 'newpassword123',
        }
        response = self.client.put(self.url, data=data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_change_password_with_mismatched_new_passwords(self):
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.blogger_token.key}',
            'content_type': 'application/json',
        }
        data = {
            'current_password': 'bloggerpass',
            'new_password': 'newpassword123',
            'confirm_password': 'mismatchedpassword',
        }
        response = self.client.put(self.url, data=json.dumps(data), **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class UpdateUserRoleTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='user', password='passworduser')
        
        self.admin = User.objects.create(username='admin', password=make_password('adminpass'))
        self.admin_role = Role.objects.create(user=self.admin, is_admin=True)
        self.admin_token = Token.objects.create(user=self.admin)

        self.moderator = User.objects.create(username='moderator', password=make_password('moderatorpass'))
        self.moderator_role = Role.objects.create(user=self.moderator, is_moderator=True)
        self.moderator_token = Token.objects.create(user=self.moderator)

        self.blogger = User.objects.create(username='blogger', password=make_password('bloggerpass'))
        self.blogger_role = Role.objects.create(user=self.blogger, is_blogger=True)
        self.blogger_token = Token.objects.create(user=self.blogger)  


        self.url = reverse('not_a_boring_blog:update_role', kwargs={'username': self.blogger.username})
        
        
    def test_update_user_role_by_admin(self):
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.admin_token.key}',
            'content_type': 'application/json',
        }
        data = {
            'role': {
                'is_blogger': False, 
                'is_moderator': False,
                'is_admin': True,
            }
        }
        response = self.client.put(self.url, data=json.dumps(data), **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    
    def test_update_user_role_by_blogger(self):
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.blogger_token.key}',
            'content_type': 'application/json',
        }
        data = {
            'role': {
                'is_blogger': False, 
                'is_moderator': True,
                'is_admin': False,
            }
        }
        response = self.client.put(self.url, data=json.dumps(data), **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update_user_role_for_nonexistent_user(self):
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.admin_token.key}',
            'content_type': 'application/json',
        }
        data = {
            'role': {
                'is_blogger': False,
                'is_moderator': False,
                'is_admin': False,
            }
        }
        url = reverse('not_a_boring_blog:update_role', kwargs={'username': 'nonexistentuser'})
        response = self.client.put(url, data=data, **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_user_role_with_invalid_data(self):
        headers = {
            'HTTP_AUTHORIZATION': f'Token {self.admin_token.key}',
            'content_type': 'application/json',
        }
        # Missing 'role' key in data
        data = {
            'is_someone': False,
            'is_noone': True,
            'is_admin': True,
        }
        response = self.client.put(self.url, data=data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)