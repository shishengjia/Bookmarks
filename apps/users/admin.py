from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username']

admin.site.register(UserProfile, UserProfileAdmin)
