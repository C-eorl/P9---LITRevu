from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from .models import User


@admin.register(User)
class UserCustomAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "profile_image_preview")
    list_filter = ("is_staff", "is_active")

    fieldsets = UserAdmin.fieldsets + (
        ("Profil", {"fields": ("profile_picture",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Profil", {"fields": ("profile_picture",)}),
    )

    def profile_image_preview(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius:50%;" />',
                               obj.profile_picture.url)
        return "-"

    profile_image_preview.short_description = "Photo"
