from rest_framework import serializers
from ..models.comment import Comment


class ReplyCommentSerializer(serializers.ModelSerializer):
    '''Serializer for reply'''
    body = serializers.CharField(max_length=500, required=True)
    class Meta:
        model = Comment
        fields = ['id', 'body', 'created_at']

    def update(self, instance, validated_data):
        # Add custom logic here, if needed
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance


class ReplyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author', 'body', 'created_at', 'parent_id']


class CommentSerializer(serializers.ModelSerializer):
    replies = ReplyDetailsSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['id', 'post_id', 'body', 'created_at', 'author', 'replies']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['replies_count'] = instance.replies.count()
        return representation