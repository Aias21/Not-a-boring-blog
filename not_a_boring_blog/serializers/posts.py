from rest_framework import serializers
from ..models.post import Category, Post
from rest_framework.exceptions import ValidationError
from django.utils.html import strip_tags
from ..models.user import Role, User
from datetime import datetime


class UniqueBodyValidator:
    def __call__(self, value):
        if Post.objects.filter(body=value).exists():
            raise ValidationError(f'Post with the same body already exists! Please choose another text')


class DateValidator:
    def __call__(self, value):
        if value > datetime.today():
            raise ValidationError(f'The date cannot be further than {datetime.today()}')


class DateField(serializers.ReadOnlyField):
    def to_representation(self, obj):
        return obj

    def to_internal_value(self, data):
        if isinstance(data, datetime):
            return data
        else:
            raise serializers.ValidationError("Invalid date format.")
    
    def run_validation(self, data):
        value = self.to_internal_value(data)
        self.run_validators(value)
        return value


class PostUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)

    class Meta:
        model = Post
        fields = ['title', 'category', 'status', 'min_read', 'description', 'body', 'created_at', 'last_updated']


class PostSerializer(serializers.ModelSerializer):
    last_updated = serializers.DateTimeField(format="%d-%B-%Y %H:%M", validators=[DateValidator()], required=False)
    title = serializers.CharField(required=True, max_length=255)
    created_at = serializers.DateTimeField(format="%d-%B-%Y %H:%M", validators=[DateValidator()], required=False)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    author = serializers.SerializerMethodField()
    bio = serializers.SerializerMethodField()
    category_names = serializers.SerializerMethodField()

    def get_bio(self, obj):
        role = Role.objects.get(user=obj.user_id)
        return role.bio
    def get_author(self, obj):
        return obj.user_id.username

    def get_category_names(self, obj):
        category_ids = [category.id for category in obj.category.all()]
        categories = Category.objects.filter(id__in=category_ids)
        return [category.category_name for category in categories]

    def validate_description(self, value):
        return strip_tags(value)

    def to_internal_value(self, data):
        if 'status' in data:
            data['status'] = 'published'
            return super().to_internal_value(data)

    class Meta:
        model = Post
        fields = ['id', 'title', 'user_id', 'author', 'bio', 'category', 'category_names', 'status',
                  'min_read', 'description', 'body', 'created_at', 'last_updated']


class PostCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField(max_length=255)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    body = serializers.CharField(validators=[UniqueBodyValidator()])  # Add UniqueBodyValidator here

    class Meta:
        model = Post
        fields = ['title', 'category', 'status', 'min_read', 'description', 'body']

    def validate_description(self, value):
        return strip_tags(value)


class HidePostSerializer(serializers.ModelSerializer):
    status = serializers.CharField(default='editing')

    class Meta:
        model = Post
        fields = ['status']
