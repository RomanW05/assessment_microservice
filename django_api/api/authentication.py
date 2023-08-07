from rest_framework.permissions import BasePermission

class HasRestrictedScope(BasePermission):
    def has_permission(self, request, view):
        try:
            request.auth.payload
        except:
            return False
        print(request.auth.payload, 'HAS RESTRICTED SCOPE')
        # Check if the 'scope' claim is present in the token payload
        if 'scope' in request.auth.payload:
            # Check if the token's scope matches the required scope ('restricted')
            return request.auth.payload['scope'] == 'restricted'

        # If 'scope' claim is not present, deny access
        return False


class HasFullScope(BasePermission):
    def has_permission(self, request, view):
        try:
            # print(request.auth.payload,'print(request.auth.payload)\n\n\n\n\n')
            # auth = request.headers['Authorization']
            request.auth.payload
        except:
            return False
        # print(request.headers['Authorization'], 'request\n\n\n\n')
        # Check if the 'scope' claim is present in the token payload
        if 'scope' in request.auth.payload:
            # Check if the token's scope matches the required scope ('restricted')
            print(request.auth.payload['scope'] == 'full', "request.auth.payload['scope'] == 'full'")
            return request.auth.payload['scope'] == 'full'

        # If 'scope' claim is not present, deny access
        return False