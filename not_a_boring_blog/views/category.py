from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.post import Category
from ..serializers.category import CategorySerializer, CategoriesSerializer
from rest_framework.permissions import IsAuthenticated


    
class CreateCategory(APIView):  
    """***This API creates a new post category.***
    
    <b>Requirements</b>:
    - The user must be registered and authenticated to create a category.
    - The user will need to use their token 
    - The category name you provide should not yet exist in the database.<p>
    ------------------------------------------------------------<p>
    ***HOW TO USE:***<p>
    <ul><b>1. AUTHENTICATION</b><p>
    <ul><b>1.1.</b>  Before making a request to this endpoint, ensure that you are authenticated, using your token. <p>
    ---> For this check <i><u>user/registration/</u></i> and <i><u>user/login</u></i>.<p>    
    <b>1.2.</b> Apply the token, it should belong to the authenticated user.<p>
    !!! For this follow the steps:<p>
    ---> click on the image of a <b>lock</b> in the right corner of your highlighted box, <p> 
    ---> choose <b><i>tokenAuth</i></b>,<p> 
    ---> insert your <b><i>token key</i></b> and <b>Authorize</b></ul></ul><p>
    ------------------------------------------------------------<p>
    <ul><b>2. BODY</b>:<p>
    <ul><b>2.1.</b> In order to add <b>json</b> information to the <b>body</b>, click on <b><i>Try it out</i></b> button<p>
    <b>2.2.</b> In the request body (application/json), provide a unique category name you wish to create in the format:<p>
        <b><i>{"category_name": "Your Category Name Here"}</i></b><p>
    <b>2.3.</b>  Press the <b><i>Execute</i></b> button in order to send a <b>POST</b> request to the API endpoint.<p>
    -- If successful, the API will return a success message along with <i><u>detail</u></i> and <i><u>category_id</u></i>. <p>
    -- If there are any errors, appropriate error messages will be returned.</ul></ul>
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