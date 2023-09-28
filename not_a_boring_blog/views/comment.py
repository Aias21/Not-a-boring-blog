from rest_framework import status, viewsets
from rest_framework.response import Response
from ..models.comment import Comment
from ..serializers.comment import CommentSerializer, ReplyCommentSerializer
from rest_framework.permissions import AllowAny
from ..permissions import IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from ..models.post import Post
from ..models.user import User
from django.http import Http404



class PostCommentList(APIView):
    """Gets all comments top-level comments (aren't replies to other comments) for a given post  - visible for everyone
    Requirements:
    - No authentication is required to retrieve the comments.

    How to use:
    - Method: GET 
    - provide the post_id of the post you want to retrieve comments for in the endpoint. 
    If there are no comments, a 404 error will be returned.
    """
    permission_classes = [AllowAny]

    def get(self, request, post_id):
        try:
            comments = Comment.objects.filter(post_id=post_id, parent_id=None)  # Retrieve top-level comments (not replies)
            if not comments.exists():
                raise Http404("No comments found")
            serializer = CommentSerializer(comments, many=True, context={'request': request})

        except Comment.DoesNotExist:
            return Response({"detail": "Comments not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateComment(APIView):
    """This API endpoint allows the creation of a new comment on a public post
    Requirements:
    - User must be authenticated to create a comment.

    How to use:
    - Method:  POST, use post_id you want to comment on in the endpoint
    """
    serializer_class = ReplyCommentSerializer

    def post(self, request, post_id):
        try:
            post = Post.objects.get(pk=post_id, status='published')  # Retrieve the associated post
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReplyCommentSerializer(data=request.data)
        if serializer.is_valid():
            # Set the comment's author to the authenticated user
            serializer.save(author=request.user, post_id=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateComment(APIView):
    """Get/ Update/ Delete comment
    Requirements:
    - User must be authenticated
    - The user can only update or delete comments they authored
    """
    serializer_class = ReplyCommentSerializer

    def get_comment(self, comment_id):
        try:
            return Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return None

    def get(self, request, comment_id):
        '''Make a GET request with the comment_id to get the details of the comment'''
        comment = self.get_comment(comment_id)
        if comment is None:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReplyCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, comment_id):
        '''Make a PUT request with the comment_id, providing the updated comment data in the request body. 
        Ensure you are the author of the comment and authenticated with the appropriate token.'''
        comment = Comment.objects.get(pk=comment_id)
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
        '''Make a DELETE request with the comment_id. 
        Ensure you are the author of the comment and authenticated.'''
        comment = Comment.objects.get(pk=comment_id)
        if comment is None:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        if comment.author != request.user:
            return Response({"detail": "You do not have permission to delete this comment"},
                                status=status.HTTP_403_FORBIDDEN)
        comment.delete()
        return Response({"detail": "Comment deleted successfully"}, status=status.HTTP_200_OK)


class CreateReply(APIView):
    '''Allows user to create a reply to a specific comment
    Requirements:
    -User must be authenticated to create a reply.
    
    How to use:
    - Method: POST, use comment_id you want to reply to to your endpoint, including the reply data in the request body. 
    '''
    serializer_class = ReplyCommentSerializer

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id)  # Retrieve the associated post
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReplyCommentSerializer(data=request.data)
        if serializer.is_valid():
            # Set the comment's author to the authenticated user
            serializer.save(author=request.user, parent_id=comment, post_id=comment.post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
