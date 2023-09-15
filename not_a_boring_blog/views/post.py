from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.post import Post
from ..serializers.posts import PostSerializer, PostCreateSerializer, PostUpdateSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from ..permissions import IsOwnerOrReadOnly
from ..models.user import Role, User


from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import permission_classes


class PostList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=200) # or status=200

class PostCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED) # or status=201
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # or status=400


class PostDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_post(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_post(pk)
        if post:
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
        if post:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_404_NOT_FOUND)

class GetPublicPosts(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        public_posts = Post.objects.filter(status='published')
        serializer = PostSerializer(public_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OnlyUserPostsView(APIView):
    def get(self, request):
        user = request.user
        try:
            role = Role.objects.get(user=user)
        except Role.DoesNotExist:
            role = None
        
        if role:
            posts = Post.objects.filter(user_id=role)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK) # or status=200
        else:
            return Response({"detail": "Role is not found for this user"}, status=status.HTTP_400_BAD_REQUEST)
