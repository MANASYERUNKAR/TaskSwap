"""Django's built-in administration views for the TaskSwap data model."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Application, PasswordResetToken, Profile, Task, TaskMessage, User


@admin.register(User)
class TaskSwapUserAdmin(UserAdmin):
    """Make the custom email user model manageable through Django admin."""

    ordering = ("email",)
    list_display = ("email", "name", "is_admin", "is_active", "created_at")
    list_filter = ("is_admin", "is_active", "is_staff")
    search_fields = ("email", "name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal information", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_admin", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2", "is_admin", "is_staff", "is_superuser"),
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Filter and review tasks in Django's standard administration interface."""

    list_display = ("title", "category", "budget", "deadline", "status", "posted_by", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title", "description", "posted_by__email", "posted_by__name")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("task", "applicant", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("task__title", "applicant__email", "applicant__name")


@admin.register(TaskMessage)
class TaskMessageAdmin(admin.ModelAdmin):
    """Allow authorised staff to review messages when resolving a moderation issue."""

    list_display = ("task", "sender", "created_at")
    search_fields = ("task__title", "sender__email", "sender__name", "body")
    list_select_related = ("task", "sender")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "skills")
    search_fields = ("user__email", "user__name", "location")


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "expires_at", "used")
    search_fields = ("user__email",)
    list_filter = ("used",)
