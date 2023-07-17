from django.db import models


class Users(models.Model):
    username = models.CharField(max_length=20, blank=False, unique=True)
    email = models.CharField(max_length=63, blank=False, unique=True)
    password = models.CharField(max_length=63, blank=False)

    def __str__(self):
        return self.username
