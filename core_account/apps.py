# core_account/apps.py

from django.apps import AppConfig

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core_account'

    def ready(self):
        import core_account.signals

