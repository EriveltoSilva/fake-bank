""" accounts admin module"""

from django.contrib import admin

from .models import Profile, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """user django admin config class"""

    list_display = [
        "full_name",
        "username",
        "email",
        "phone",
        "is_staff",
        "is_active",
        "date_joined",
        "last_login",
    ]
    list_display_links = [
        "full_name",
        "username",
        "email",
        "phone",
        "is_staff",
        "is_active",
        "date_joined",
        "last_login",
    ]
    search_fields = ["full_name", "username", "email", "phone"]
    list_per_page = 25


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """profile django admin config class"""

    list_display = ["full_name", "gender", "birthday", "country", "state", "city", "address", "created_at"]
    list_display_links = ["full_name", "gender", "birthday", "country", "state", "city", "address", "created_at"]
    search_fields = ["full_name", "gender", "birthday", "country", "state", "city", "address"]
    list_filter = ["gender"]
    list_per_page = 25
