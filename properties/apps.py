from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self):
        # Import signals to connect them
        import properties.signals
        
default_app_config = 'properties.PropertiesConfig'