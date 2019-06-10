from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
     def has_object_permission(self, request, view, obj):
         if request.method in permissions.SAFE_METHODS:
             return True
        # 对象是自己的才能操作
         return obj.owner == request.user