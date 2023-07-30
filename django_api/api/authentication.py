from rest_framework.permissions import BasePermission

class HasRestrictedScope(BasePermission):
    def has_permission(self, request, view):
        print(request.auth.payload)
        # Check if the 'scope' claim is present in the token payload
        if 'scope' in request.auth.payload:
            # Check if the token's scope matches the required scope ('restricted')
            return request.auth.payload['scope'] == 'restricted'

        # If 'scope' claim is not present, deny access
        return False


class HasFullScope(BasePermission):
    def has_permission(self, request, view):

        # Check if the 'scope' claim is present in the token payload
        if 'scope' in request.auth.payload:
            # Check if the token's scope matches the required scope ('restricted')
            return request.auth.payload['scope'] == 'full'

        # If 'scope' claim is not present, deny access
        return False