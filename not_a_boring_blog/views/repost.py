from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from ..permissions import IsOwnerOrReadOnly
from ..models.repost_request import RepostRequest, Post, User, Role
from ..serializers.repost import (
    RepostSerializer,
    RepostRequestListSerializer,
    UpdateRepostRequestSerializer,
)


class CreateRepostRequest(APIView):
    """Creates Repost Request"""
    serializer_class = RepostSerializer

    def post(self, request, post_id):
        # Check if the user has already created a repost request for the same post
        existing_request = RepostRequest.objects.filter(
            requester_id=request.user.id,
            post_id=post_id,
        ).first()

        if existing_request:
            return Response(
                {"detail": "You have already created a repost request for this post."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create a serializer instance with the provided request data
        serializer_data = {
            **request.data,
            'requester_id': request.user.id,
            'post_id': post_id,
        }
        serializer = RepostSerializer(data=serializer_data)

        if serializer.is_valid():
            # Create the repost request
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RepostRequestedReceivedList(APIView):
    """Returns requests to post author"""

    def get(self, request):
        # Get the authenticated user (post owner)
        user = self.request.user
        # Filter repost requests for posts owned by the user
        queryset = RepostRequest.objects.filter(post_id__user_id=user.id)
        # Serialize the queryset
        serializer = RepostRequestListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RepostRequestsSentList(APIView):
    """Returns requests sent by user"""

    def get(self, request):
        user = self.request.user
        # Filter repost requests for requests owned by the user
        queryset = RepostRequest.objects.filter(requester_id=user.id)
        # Serialize the queryset
        serializer = RepostRequestListSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateRepostRequestStatus(APIView):
    """Post author can update the status of a request by id - updates status to accepted or denied"""
    serializer_class = UpdateRepostRequestSerializer

    def put(self, request, request_id):
        # Get the authenticated user (post owner)
        user = self.request.user

        try:
            # Retrieve the repost request by request id and check if it belongs to the user
            repost_request = RepostRequest.objects.get(id=request_id, post_id__user_id=user.id)
        except RepostRequest.DoesNotExist:
            return Response({"detail": "Repost request not found for this user"}, status=status.HTTP_404_NOT_FOUND)

        # Create an instance of the update serializer with the repost request data
        serializer = UpdateRepostRequestSerializer(repost_request, data=request.data)

        if serializer.is_valid():
            # Update the status if it's a valid choice ("approved" or "denied")
            new_status = serializer.validated_data['status'].lower()
            if new_status in ['approved', 'denied']:
                repost_request.status = new_status
                repost_request.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "Invalid status choice"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteRepostRequestView(APIView):
    """Requester can delete a request by id"""
    def delete(self, request, request_id):
        # Get the authenticated user (post owner)
        user = self.request.user

        try:
            # Retrieve the repost request by request_id and check if it belongs to a post owned by the user
            repost_request = RepostRequest.objects.get(id=request_id, requester_id=user.id)
        except RepostRequest.DoesNotExist:
            return Response({"detail": "Repost request not found"}, status=status.HTTP_404_NOT_FOUND)

        # Ensure that repost_request is a valid RepostRequest instance
        if isinstance(repost_request, RepostRequest):
            # Delete the repost request
            repost_request.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({"detail": "Invalid repost request"}, status=status.HTTP_400_BAD_REQUEST)