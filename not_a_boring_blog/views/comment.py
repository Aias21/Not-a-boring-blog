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


class PostCommentList(APIView):
    '''Gets all comments, visible for everyone'''
    permission_classes = [AllowAny]

    def get(self, request, post_id):
        try:
            comments = Comment.objects.filter(post_id=post_id, parent_id=None)  # Retrieve top-level comments (not replies)
            serializer = CommentSerializer(comments, many=True, context={'request': request})
        except Comment.DoesNotExist:
            return Response({"detail": "Comments not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateComment(APIView):
    '''Create comment, only authenticated users can do it'''
    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id)  # Retrieve the associated post
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReplyCommentSerializer(data=request.data)
        if serializer.is_valid():
            # Set the comment's author to the authenticated user
            serializer.save(author=request.user, post_id=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateComment(APIView):
    '''Update/Delete comment, only authenticated users can do this that are also authors'''
    permission_classes = [IsAuthenticated]

    def get_comment(self, comment_id):
        try:
            return Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return None

    def get(self, request, comment_id):
        comment = self.get_comment(comment_id)
        if comment is None:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReplyCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, comment_id):
        comment = self.get_comment(comment_id)
        if comment is None:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReplyCommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            # Check if the user making the request is the author of the comment.
            if comment.author != request.user:
                return Response({"detail": "You do not have permission to update this comment"}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id):
        comment = self.get_comment(comment_id)
        if comment is None:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        if comment.author != request.user:
            return Response({"detail": "You do not have permission to delete this comment"},
                                status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({"detail": "Comment deleted successfully"}, status=status.HTTP_200_OK)


class CreateReply(APIView):
    '''Create reply, only authenticated users can do this'''

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)  # Retrieve the associated post
        except Post.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReplyCommentSerializer(data=request.data)
        if serializer.is_valid():
            # Set the comment's author to the authenticated user
            serializer.save(author=request.user, parent_id=comment, post_id=comment.post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
