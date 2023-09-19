from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.post import Category
from ..serializers.category import CategorySerializer
from rest_framework.permissions import IsAuthenticated


class CreateCategory(APIView):
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