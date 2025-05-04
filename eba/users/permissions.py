from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    
    def has_permission(self,request,view):
        return request.user.is_moderator