from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    
    def has_permission(self,request,view):
        print("here it is :",request.user.is_moderator)
        return request.user.is_moderator