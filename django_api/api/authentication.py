from rest_framework.permissions import BasePermission

class HasRestrictedScope(BasePermission):
    def has_permission(self, request, view):
        # Check if the 'scope' claim is present in the token payload
        if 'scope' in request.auth.payload:
            # Check if the token's scope matches the required scope ('restricted')
            return request.auth.payload['scope'] == 'restricted'

        # If 'scope' claim is not present, deny access
        return False

from oauth2_provider.contrib.rest_framework import TokenHasScope
class TokenHasScopeForMethod(TokenHasScope):

     def has_permission(self, request, view):
         token = request.auth

         if not token:
             return False

         if hasattr(token, "scope"):
             # Get the scopes required for the current method from the view
             required_scopes = view.required_scopes_per_method[request.method]

             return token.is_valid(required_scopes)