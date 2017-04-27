from django.apps import AppConfig


class ImageConfig(AppConfig):
    name = 'image'

    def ready(self):
        import image.signals
