from django.apps import AppConfig


class DriversConfig(AppConfig):
    name = 'drivers'

    def ready(self):
        from drivers import tasks
        tasks.star()
