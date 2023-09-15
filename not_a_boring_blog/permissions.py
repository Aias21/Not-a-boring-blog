from rest_framework import permissions


# to handle ownership-based permissions. 
# This class should check if the user making the request is the owner of the post.
class IsOwnerOrReadOnly(permissions.BasePermission):
    SAFE_METHODS = ["GET", "PUT"]

    def has_object_permission(self, request, view, obj):     
        if request.method in self.SAFE_METHODS:
            if obj.user_id.user == request.user or obj.status == 'published':                
                return True
        return False