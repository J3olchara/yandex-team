from django.apps import AppConfig


class AuthorisationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authorisation'
    label = 'users'

    def ready(self) -> None:
        import authorisation.signals

        authorisation.signals.forward()
