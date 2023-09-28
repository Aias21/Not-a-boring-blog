from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.post import Post
from ..serializers.posts import (
    PostSerializer, 
    PostCreateSerializer, 
    PostUpdateSerializer
    )
from ..permissions import IsOwnerOrReadOnly, IsAdminRole, IsModeratorRole
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models.user import Role, User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.generics import ListAPIView
from django.shortcuts import get_object_or_404, get_list_or_404


class PostList(APIView):
    """Lists all posts irrespective of their status.
    Requirements:
    - Must be authenticated.
    - Must have an admin or moderator role.
    
    How to use:
    - Method: GET
    - Authorization: Token {token(admin or moderator)}
    """
    permission_classes = [IsAuthenticated, IsAdminRole | IsModeratorRole]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=200) # or status=200


class PostCreate(APIView):
    '''Allows the creation of a new post.
    Requirements:
    - Must be authenticated.
    
    How to use:
    - Method: POST
    - Authorization: Token {token(any authenticated user)}
    - Body: Data related to the post in JSON format.
    '''
    
    serializer_class = PostCreateSerializer

    def post(self, request):
        user_id = request.user.id  # Get the user_id from the request
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_id_id=user_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class PostDetail(APIView):
    '''Provides detailed view of a post. 
    Also allows for updating and deleting a post.
    
    Requirements:
    - Must be owner of the post.
    '''
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = PostUpdateSerializer

    def get_post(self, pk):        
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        '''How to use (retrieve a Post):
        - Method: GET
        - Authorization: Token {token(post owner)}
        '''      
        post = self.get_post(pk)
        if post:
            if not IsOwnerOrReadOnly().has_object_permission(request, self, post):
                return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            serializer = PostSerializer(post)            
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        '''How to use (update a Post):
        - Method: PUT
        - Authorization: Token {token(post owner)}
        - Body: Updated post data in JSON format.
        '''
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
        '''How to use (delete a Post):
        - Method: DELETE
        - Authorization: Token {token(post owner)}
        '''
        post = self.get_post(pk)
        if post and post.user_id == request.user:
            post.delete()
            return Response({"detail": "Deletion is done"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)


class GetPublicPosts(APIView):
    '''Fetches all posts that have the status "published"
    Requirements:
    - Open to all
    
    How to use:
    - Method: GET
    '''
    permission_classes = [AllowAny]

    def get(self, request):
        public_posts = Post.objects.filter(status='published')
        serializer = PostSerializer(public_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetUserPublicPosts(APIView):
    '''Fetches all published posts of a specified user
    Requirements:
    - Open to all
    
    How to use:
    - Method: GET
    '''
    serializer_class = PostSerializer
    permission_classes = [AllowAny]


    def get_queryset(self):
        username = self.kwargs['username']
        user = get_object_or_404(User, username=username)
        return Post.objects.filter(user_id=user, status='published')
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({"detail": f"{self.kwargs['username']} has no posts"}, status.HTTP_200_OK)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class GetUserPosts(ListAPIView):
    '''The user can see only his/her own posts
    Requirements:
    - Must be authenticated
    
    How to use:
    -Method: GET
    - Authorization: Token {token(authenticated post author)}
    '''
    serializer_class = PostSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Post.objects.filter(user_id=user)
        get_list_or_404(queryset)
        return queryset
    
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
