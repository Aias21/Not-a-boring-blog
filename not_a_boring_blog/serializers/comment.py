from rest_framework import serializers
from ..models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

    def update(self, instance, validated_data):
        # Add custom logic here, if needed
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance


class ReplyCommentSerializer(serializers.ModelSerializer):
    reply = CommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = ['post_id', 'body', 'created_at', 'author', 'parent_id','reply']