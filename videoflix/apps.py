from django.apps import AppConfig


class VideoflixConfig(AppConfig):
    name = 'videoflix'

    def ready(self):
        import videoflix.signals