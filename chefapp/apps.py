from django.apps import AppConfig


class ChefappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chefapp'
    def ready(self):
        import chefapp.signals
