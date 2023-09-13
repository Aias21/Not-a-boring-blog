from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models.comment import Comment
from ..serializers.comment import CommentSerializer, ReplyCommentSerializer
from rest_framework.permissions import AllowAny
from ..permissions import IsCommentAuthorOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..models.post import Post
from ..models.user import User


class CommentList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, post_id):
        try:
            comments = Comment.objects.filter(post_id=post_id, parent_id=None)  # Retrieve top-level comments (not replies)
            serializer = ReplyCommentSerializer(comments, many=True, context={'request': request})
        except Comment.DoesNotExist:
            return Response({"detail": "Comments not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateComment(APIView):
    pass