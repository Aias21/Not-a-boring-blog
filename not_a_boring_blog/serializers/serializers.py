from rest_framework import serializers
from ..models.post import Category, Post
from rest_framework.exceptions import ValidationError
from datetime import date, datetime
from django.utils.html import strip_tags


# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'

# class PostSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = '__all__'


class UniqueTitleValidator:
    def __call__(self, value):
        if Post.objects.filter(title=value).exists():
            raise ValidationError(f'Post with title "{value}" already exists! Please choose another title')


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
        # elif isinstance(data, date):
        #     return data.date()
        else:
            raise serializers.ValidationError("Invalid date format.")
        # if isinstance(data, datetime):
        #     return data.date()
        # return super().to_internal_value(data)
    
    def run_validation(self, data):
        value = self.to_internal_value(data)
        self.run_validators(value)
        return value

# class Capitalize:
#     def __call__(self, value):
#         return value.title()




class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'user_id', 'category', 'status', 'min_read', 'description', 'body',  'created_at', 'last_updated']


class PostSerializer(serializers.ModelSerializer):
    last_updated = serializers.DateTimeField(validators=[DateValidator()])
    title = serializers.CharField(required=True, max_length=255, validators=[UniqueTitleValidator()])
    created_at = serializers.DateTimeField(validators=[DateValidator()])

    def validate_description(self, value):
        return strip_tags(value)

    # def to_representation(self, instance):
    #     instance.title = Capitalize()(instance.title)
    #     return super().to_representation(instance)

    def to_internal_value(self, data):
        if 'status' in data:
            data['status'] = 'Published'
            return super().to_internal_value(data)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'status', 'created_at', 'last_updated']
