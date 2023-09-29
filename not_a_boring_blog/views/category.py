from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.post import Category
from ..serializers.category import (
    CategoryFilterSerializer,
    CategorySerializer,
    CategoriesSerializer
)
from ..serializers.posts import PostSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..models.post import Post
from django.db.models import Count


class CreateCategory(APIView):
    """Creates post category"""
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            # Check if the category already exists
            name = serializer.validated_data['category_name']
            existing_category = Category.objects.filter(category_name=name).first()

            if existing_category:
                return Response({'detail': 'Category already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            # Create the category
            category = serializer.save()
            return Response({'detail': 'Category created successfully.', 'category_id': category.id}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCategories(APIView):
    """Lists existing categories"""
    permission_classes = [AllowAny]
    serializer_class = CategoriesSerializer

    # def get(self, request):
    #     categories = Category.objects.all()
    #     serializer = CategoriesSerializer(categories, many=True)
    #     return Response(serializer.data, status=200)

    def get(self, request):
        # Annotate each category with the count of related posts
        categories = Category.objects.annotate(num_posts=Count('posts'), num_published_posts=Count('posts'))

        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data, status=200)


class PostsByCategory(APIView):
    permission_classes = [AllowAny]

    def get(self, request, category_name):
        try:
            category = Category.objects.get(category_name=category_name.title())
            posts = Post.objects.filter(category=category, status='published')
            if len(posts) == 0:
                return Response({"detail": f"No posts found in '{category}' category!"}, status=status.HTTP_404_NOT_FOUND)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"detail": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
