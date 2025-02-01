from django.apps import AppConfig


class WomenConfig(AppConfig):
    verbose_name = "Женщины мира"  # имя для админ панели
    default_auto_field = "django.db.models.BigAutoField"
    name = "women"
