from rest_framework import permissions


# to handle ownership-based permissions. 
# This class should check if the user making the request is the owner of the post.
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):     
        if request.method in self.SAFE_METHODS:
            if obj.user_id.user == request.user or obj.status == 'published':                
                return True
        return False


class IsAdminRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role.is_admin


class IsModeratorRole(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role.is_moderator

      
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the request user is the author of the comment.
        return obj.author == request.user

