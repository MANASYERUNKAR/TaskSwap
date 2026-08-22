from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Register the core application and its model signals."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
