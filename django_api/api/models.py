from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }


# class BlackListedToken(models.Model):
#     token = models.CharField(max_length=500)
#     user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ("token", "user")

# class RevokedToken(models.Model):
#     token = models.CharField(max_length=255, unique=True)

#     def __str__(self):
#         return self.token

#     class Meta:
#         verbose_name_plural = "Revoked Tokens"


# class IsTokenValid(BasePermission):
#     def has_permission(self, request, view):
#         user_id = request.user.id            
#         is_allowed_user = True
#         token = request.auth.decode("utf-8")
#         try:
#             is_blackListed = BlackListedToken.objects.get(user=user_id, token=token)
#             if is_blackListed:
#                 is_allowed_user = False
#         except BlackListedToken.DoesNotExist:
#             is_allowed_user = True
#         return is_allowed_user