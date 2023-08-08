from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import BlacklistMixin

class HasRestrictedScope(BasePermission):
    def has_permission(self, request, view):
        try:
            request.auth.payload
        except:
            return False
        # Check if the 'scope' claim is present in the token payload
        if 'scope' in request.auth.payload:
            # Check if the token's scope matches the required scope ('restricted')
            return request.auth.payload['scope'] == 'restricted'

        # If 'scope' claim is not present, deny access
        return False


class HasFullScope(BasePermission):
    def has_permission(self, request, view):
        try:
            request.auth.payload
        except:
            return False
        # Check if the 'scope' claim is present in the token payload
        if 'scope' in request.auth.payload:
            # Check if the token's scope matches the required scope ('restricted')
            return request.auth.payload['scope'] == 'full'

        # If 'scope' claim is not present, deny access
        return False
    

class IsWhitelisted(BasePermission):
    def has_permission(self, request, view):
        try:
            request.auth
        except:
            return False
        # BlacklistMixin.check_blacklist raises error if token is blacklisted
        try:
            BlacklistMixin.check_blacklist(request.auth)
            return True
        except:
            return False
