from rest_framework import serializers
from ..models.post import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'category_name']


class CategoryFilterSerializer(serializers.Serializer):
    category_id = serializers.CharField(max_length=255)