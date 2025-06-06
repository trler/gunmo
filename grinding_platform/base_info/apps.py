from django.apps import AppConfig


class BaseInfoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'base_info'
    verbose_name = '基础信息库' 