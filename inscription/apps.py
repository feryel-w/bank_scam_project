# apps.py
from django.apps import AppConfig

class InscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'inscription'

    # Remove/comment this:
    # def ready(self):
    #     import inscription.signals
