from ..models.user import Role
from ..models.post import Post
from ..models.views import View
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import permissions, status
from datetime import datetime, timedelta, timezone
from not_a_boring_blog.serializers.view import ViewCountSerializer


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def record_post_view(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    cooldown_period = timedelta(minutes=int(post.min_read))

    if post.user_id == user.id:
        return Response({"message": "Author's own view is not counted"})

    last_view = View.objects.filter(post_id=post.id, user_id=user.id).order_by('-timestamp').first()

    if not last_view or (datetime.now(timezone.utc) - last_view.timestamp) > cooldown_period:
        role = get_object_or_404(Role, id=user.id)
        View.objects.create(post_id=post, user_id=role)

        return Response({"message": "View recorded successfully"})

    return Response({"error": "Cooldown period not elapsed"}, status=429)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def get_post_view_count(request, post_id):
    post_views = View.objects.filter(post_id=post_id).count()
    data = {"view count": post_views}
    serializer = ViewCountSerializer(data)
    return Response(data)
