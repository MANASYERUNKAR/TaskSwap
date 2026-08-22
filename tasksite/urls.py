"""Top-level URL configuration for TaskSwap."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Built-in Django administration remains available for superusers.
    path("django-admin/", admin.site.urls),
    # The product's separately protected moderation dashboard lives under /admin/.
    path("", include("core.urls")),
]
