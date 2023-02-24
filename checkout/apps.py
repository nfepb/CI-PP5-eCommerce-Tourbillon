"""checkout app.py"""
from django.apps import AppConfig


class CheckoutConfig(AppConfig):
    """App config for checkout app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout'

    def ready(self):
        """checkout signals"""
        import checkout.signals
