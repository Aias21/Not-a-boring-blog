# # pip install djangorestframework



# class BlogList(generics.ListAPIView):
#     queryset = models.Post.objects.filter(user_id = self.request.user.id)
#     serializer_class = serializers.PostSerializer

#     def get_queryset(self):
#         return Post.objects.filter(user_id=self.kwargs['user_id'])


# from rest_framework import generics
# from .models import Post
# from .serializers import PostSerializer

# class PostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all()  # You can adjust this queryset as needed.
#     serializer_class = PostSerializer

#     def perform_create(self, serializer):
#         serializer.save(user_id=self.request.user)  # Set the user when creating a post



from rest_framework import generics
from rest_framework import permissions
from ..models.post import Post
from ..serializers.serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly

# for listing and creating posts
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)

# for retrieving, updating and deleting posts
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]



