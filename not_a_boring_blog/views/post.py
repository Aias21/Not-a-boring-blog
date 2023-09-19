from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.post import Post
from ..serializers.posts import (
    PostSerializer, 
    PostCreateSerializer, 
    PostUpdateSerializer, 
    PostTitleSerializer, 
    OnlyUserPostSerializer)
from ..permissions import IsOwnerOrReadOnly, IsAdminRole, IsModeratorRole
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models.user import Role, User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import permission_classes


class PostList(APIView):
    '''Entire post list, only admins can see the list'''
    permission_classes = [IsAuthenticated, IsAdminRole, IsModeratorRole]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=200) # or status=200

      
class PostCreate(APIView):
    '''Post creation view'''
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) # or status=201
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # or status=400


class PostDetail(APIView):
    '''Post Detail view for get, update, delete'''
    permission_classes = [IsOwnerOrReadOnly]

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_post(pk)
        if post:
            if not IsOwnerOrReadOnly().has_object_permission(request, self, post):
                return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            serializer = PostSerializer(post)            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        post = self.get_post(pk)
        if post:
            if str(request.user) != str(post.user_id):
                return Response({"detail": "Permission denied"}, status=403)
            serializer = PostUpdateSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                categories = request.data['category']
                post.update_categories(categories)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        post = self.get_post(pk)
        if post and post.user_id.user == request.user:
            post.delete()
            return Response({"detail": "Deletion is done"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Permission denied"}, status=403)

      
class GetPublicPosts(APIView):
    '''You get only published  posts of every user'''
    permission_classes = [AllowAny]

    def get(self, request):
        public_posts = Post.objects.filter(status='published')
        serializer = PostSerializer(public_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserPublicPosts(APIView):
    '''You get only published  posts of a specific user'''

    serializer_class = PostTitleSerializer
    permission_classes = [AllowAny]


    def get_queryset(self):
        username = self.kwargs['username']
        role = get_object_or_404(Role, user__username=username)
        return Post.objects.filter(user_id=role, status='published')
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class GetUserPosts(ListAPIView):
    '''The user can see only his/her own posts'''
    serializer_class = OnlyUserPostSerializer
    
    def get_queryset(self):
        user = self.request.user
        role = user.role
        queryset = Post.objects.filter(user_id=role)
        get_list_or_404(queryset)
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
