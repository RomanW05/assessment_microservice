from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    verified = models.IntegerField(null=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    otp = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.username

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

