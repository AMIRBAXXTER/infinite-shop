from django.apps import AppConfig


class ProductsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ProductsApp'

    def ready(self):
        import ProductsApp.signals
