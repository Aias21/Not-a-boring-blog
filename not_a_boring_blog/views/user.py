from rest_framework.views import APIView
from not_a_boring_blog.models.user import Role
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import User
from not_a_boring_blog.serializers.user import (
    RoleSerializer,
    CustomUserSerializer,
    LoginUserSerializer,
    UpdateRoleSerializer,
    ChangePasswordSerializer,
    UpdateUserSerializer,
)
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
)
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q


class UserList(APIView):
    """Returns the entire list of users on the platform - for Admin use"""

    # permission_classes = [AllowAny]

    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserRole(APIView):
    """Updating user role - only admin should be able to do this operation"""
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateRoleSerializer

    def put(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role.is_admin:
            serializer = UpdateRoleSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"details":"You do not have permission for this operation"}, status=status.HTTP_403_FORBIDDEN)


class RegisterUser(APIView):
    """User registration - all users should be allowed to register"""
    permission_classes = [AllowAny]
    serializer_class = CustomUserSerializer

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            username = serializer.validated_data.get('username')
            
            # Check if a user with the same email or username already exists
            if User.objects.filter(Q(username=username)).exists():
                return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
            elif User.objects.filter(Q(email=email)).exists():
                return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Hash the password and save the user
            user = serializer.save()
            return Response({"message": "Registration successful."}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateUser(APIView):
    """Update user information - username, email and bio, user needs to be authorized"""
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer

    def put(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            role = Role.objects.get(user=user)  # Get the Role associated with the user
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        except Role.DoesNotExist:
            return Response({"detail": "Role not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateUserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # Update the 'bio' field in the associated Role model
            if 'bio' in request.data:
                role.bio = request.data['bio']
                role.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangeUserPassword(APIView):
    """Change user password - user needs to be authorized"""
    serializer_class = ChangePasswordSerializer

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get('current_password')):
                user.set_password(serializer.data.get('new_password'))
                user.save()
                update_session_auth_hash(request, user)  # To update session after password change
                return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
            return Response({'error': 'Incorrect old password.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUser(APIView):
    """Login user - can be done with username or email, token is created.
    All authorized actions require this token"""
    permission_classes = [AllowAny]
    serializer_class = LoginUserSerializer

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data.get("username") or serializer.data.get("email"):
                username = ''
                email = ''
                if serializer.data.get("username"):
                    username = serializer.data.get("username").lower()
                if serializer.data.get("email"):
                    email = serializer.data.get("email").lower()
                try:
                    user_exists = User.objects.filter(
                        Q(username=username) | Q(email=email)).first()
                except User.DoesNotExist:
                    return Response({"detail": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({"detail": "You need to provide username or email in order to log in!"})
            password = serializer.data.get("password")
            user = authenticate(username=user_exists, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                try:
                    role = Role.objects.get(user=user)
                    role_serializer = RoleSerializer(role)
                    true_roles = {}  # Dictionary key-value pairs of true roles
                    for key, value in role_serializer.data.items():
                        if value:
                            true_roles[key] = value
                except Role.DoesNotExist:
                    true_roles = None
                data = {
                    "token": str(token),
                    "username": str(user_exists),
                    "role": true_roles
                }
                return Response(data, status=200)
            else:
                return Response({"detail": "Wrong credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutUser(APIView):
    """Logout user - token is destroyed"""
    def get(self, request, format=None):
        # simply delete the token to force a logout
        try:
            request.user.auth_token.delete()
            return Response({"detail": f"Goodbye, {request.user}!"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "You are not logged in!"}, status=status.HTTP_404_NOT_FOUND)