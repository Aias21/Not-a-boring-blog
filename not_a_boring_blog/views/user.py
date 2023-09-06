from rest_framework.views import APIView
from ..models.user import Role
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from ..serializers.user import RoleSerializer, CustomUserSerializer, LoginUserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password


class UserList(APIView):
    # permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterUser(APIView):
    permission_classes = [AllowAny] #  allow any user to register

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            Token.objects.create(user=user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class UpdateUser(APIView):
    authentication_classes = [TokenAuthentication]

    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        # Check if updated user is the same as the authenticated user
        if request.user != user:
            return Response({"detail": "Permission denied"},status=status.HTTP_403_FORBIDDEN)
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            new_password = request.data.get("password")
            if new_password:
                user.set_password(new_password)
                user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        password = request.data.get('password')
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data.get("username").lower()
            user = authenticate(username=username, password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                data = {"token": str(token), "username": username}
                return Response(data, status=200)
            return Response(serializer.errors)