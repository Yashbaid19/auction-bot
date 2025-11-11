from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'phone_number', 'is_active', 'is_staff', 'created_at']
    list_filter = ['is_staff', 'is_active', 'created_at']
    search_fields = ['username', 'email']
    ordering = ['-created_at']

