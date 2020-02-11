"""admin for users_api module"""
from django.contrib import admin
from users_api import models

admin.site.register(models.UserProfile)
