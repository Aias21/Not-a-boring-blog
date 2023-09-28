from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.post import Category
from ..serializers.category import CategorySerializer, CategoriesSerializer
from rest_framework.permissions import IsAuthenticated


    
class CreateCategory(APIView):  
    """This API creates a post category.
    Requirements:
    - The user must be authenticated to create a category.
    - The category name provided should not yet exist in the database.
    
    How to use:
    - Make a POST request to the API endpoint.
    - Attach the authentication token in the header to ensure you're authenticated. 
    The token should belong to an authenticated user.
    - In the request body, provide the category name you wish to create in the format:
        {"category_name": "Your Category Name Here"}
    - If successful, the API will return a success message along with the category ID. 
    If there are any errors, appropriate error messages will be returned.
    """ 
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
    """This API lists all the existing post categories.
    Requirements:
    - There are no authentication requirements to list the categories.
    
    How to use:
    - Make a GET request to the API endpoint.
    - No authentication token or additional headers are needed.
    - The API will return a list of all existing categories in the database.
    """
    serializer_class = CategoriesSerializer

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategoriesSerializer(categories, many=True)
        return Response(serializer.data, status=200)