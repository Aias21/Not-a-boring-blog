from rest_framework import serializers
from ..models.user import Role
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

class UniqueUsernameValidator:
    def __call__(self, value):
        if User.objects.filter(username=value).exists():
            raise ValidationError(f'Username already exists!')


class UniqueEmailValidator:
    def __call__(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError(f'Email already exists!')


class RoleSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(max_length=255, allow_blank=True, required=False)

    class Meta:
        model = Role
        fields = ['is_moderator', 'is_blogger', 'is_admin', 'bio']

    def validate(self, data):
        is_moderator = data.get('is_moderator', False)
        is_blogger = data.get('is_blogger', False)
        is_admin = data.get('is_admin', False)

        # Ensure that only one of the three boolean values is True
        if sum([is_moderator, is_blogger, is_admin]) != 1:
            raise serializers.ValidationError("Only one attribute can be True at a time!")

        return data


class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    role = RoleSerializer(default={'is_blogger': True})  # Embed the RoleSerializer
    email = serializers.EmailField(required=True)
    password = serializers.CharField( required=True, style={'input_style': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'role']

    def create(self, validated_data):
        role_data = validated_data.pop('role')  # Extract role data
        user = User.objects.create(
            username=validated_data['username'].lower(),
            email=validated_data['email'].lower(),
            password=make_password(validated_data['password'])
        )
        Role.objects.create(user=user, **role_data)  # Create a Role instance associated with the user
        return user

    def update(self, instance, validated_data):
        role_data = validated_data.pop('role', {})  # Extract role data
        role_instance = instance.role  # Get the existing role instance

        # Update user fields
        instance.username = validated_data.get('username', instance.username).lower()
        instance.email = validated_data.get('email', instance.email).lower()

        # If the username or email has changed, check for conflicts
        if 'username' in validated_data or 'email' in validated_data:
            try:
                if 'username' in validated_data:
                    existing_user = User.objects.get(username=validated_data['username'])
                    if existing_user != instance:
                        raise serializers.ValidationError("Username already exists.")
                if 'email' in validated_data:
                    existing_user = User.objects.get(email=validated_data['email'])
                    if existing_user != instance:
                        raise serializers.ValidationError("Email already exists.")
            except User.DoesNotExist:
                pass  # No conflicts found, continue updating

        # Update role fields
        role_instance.is_moderator = role_data.get('is_moderator', role_instance.is_moderator)
        role_instance.is_blogger = role_data.get('is_blogger', role_instance.is_blogger)
        role_instance.is_admin = role_data.get('is_admin', role_instance.is_admin)
        role_instance.bio = role_data.get('bio', role_instance.bio)

        instance.save()
        role_instance.save()
        return instance


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True, required=True, style={'input_style': 'password'})
    role = RoleSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['username',  'password', 'role']

    def to_representation(self, instance):
        # Remove the 'role' field for false values
        data = super().to_representation(instance)
        print(data)
        role_data = data.get('role')
        print(role_data)
        if role_data and not any(role_data.values()):
            data.pop('role')
        return data