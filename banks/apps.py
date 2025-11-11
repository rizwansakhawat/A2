from django.apps import AppConfig

import banks


class BanksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'banks'
    
    def ready(self):
        from . import signals
