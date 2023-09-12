from rest_framework import permissions


# to handle ownership-based permissions. 
# This class should check if the user making the request is the owner of the post.


# there is sth wrong with it
class IsOwnerOrReadOnly(permissions.BasePermission):
    SAFE_METHODS = ["GET", "PUT", "DELETE"]
    def has_object_permission(self, request, view, obj):
        print(request.method in permissions.SAFE_METHODS)
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user_id == request.user


