from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
     def has_object_permission(self, request, view, obj):
         if request.method in permissions.SAFE_METHODS:
             return True
        # 对象是自己的才能操作
         return obj.owner == request.user



class CustomerAccessPermission(permissions.BasePermission):
    """
    自定义权限控制
    """
    def has_permission(self, request, view):
        method = request.method
        if method == "GET":
            return True
        elif method == "POST":
            print("post is allow!")
            return True
        else:
            print("other method is allow!")
            return True