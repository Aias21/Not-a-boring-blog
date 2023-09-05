from rest_framework import generics
from rest_framework import permissions
from ..models.post import Post
from ..serializers.serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly
from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import View



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


class ArticleListView(View):
    def get(self, request):
        articles = Post.objects.all()
        template = loader.get_template('list_post.html')
        context = {'articles': articles}
        return HttpResponse(template.render(context, request))


# class ArticleListView(View):
#     template_name = 'list_post.html'  # Specify the template path

#     def get(self, request):
#         articles = Post.objects.all()
#         context = {'articles': articles}
#         return render(request, self.template_name, context)
