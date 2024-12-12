from rest_framework import permissions

class ProfilePermissiom(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        '''
        リクエストメソッドが、GETやCREATEの非破壊的メソッドの場合は、True
        リクエストメソッドが、DeleteやPUTの破壊的メソッドの場合は、Falseを返す
        '''
        if request.method in permissions.SAFE_METHODS:
            return True
        return False
