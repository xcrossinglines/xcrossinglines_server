from django.apps import AppConfig


class QuotejobsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quotejobs'

    #... 
    def ready(self):
        import quotejobs.signals
