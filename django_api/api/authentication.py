
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from .models import RevokedToken
# from rest_framework.exceptions import AuthenticationFailed

# class CustomJWTAuthentication(JWTAuthentication):
#     def authenticate(self, request):
#         try:
#             user, token = super().authenticate(request)
#         except AuthenticationFailed as af:
#             raise af

#         if self.is_token_revoked(token):
#             raise AuthenticationFailed("Invalid token.")

#         return user, token

#     def is_token_revoked(self, token):
#         return RevokedToken.objects.filter(token=token).exists()