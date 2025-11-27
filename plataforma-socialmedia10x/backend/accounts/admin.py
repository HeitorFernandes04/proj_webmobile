# backend/accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User  # seu modelo custom de usuário


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Admin do usuário.
    Você pode customizar os fieldsets depois, se quiser.
    """
    pass
