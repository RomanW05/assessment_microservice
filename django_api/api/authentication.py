from rest_framework.permissions import BasePermission

class RestrictedScopePermission(BasePermission):
    def has_permission(self, request, view):
        # Check if the 'scope' claim is present in the token payload
        if 'scope' in request.auth:
            # Restrict access if the 'scope' is not 'restricted'
            return request.auth['scope'] == 'restricted'

        # If 'scope' claim is not present, deny access
        return False

