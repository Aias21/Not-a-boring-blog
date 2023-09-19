from rest_framework import permissions


# to handle ownership-based permissions. 
# This class should check if the user making the request is the owner of the post.
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the request user is the author of the comment.
        return obj.author == request.user
