from django.contrib import admin
from .models import Users
from django.contrib.auth.models import Group

admin.site.register(Users)
admin.site.unregister(Group)

admin.site.site_header = "API admin"