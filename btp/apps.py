from django.apps import AppConfig


# class BtpConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'btp'

# from django.apps import AppConfig

class BtpConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'btp'

    def ready(self):
        from django.contrib.auth.models import Group

        Group.objects.get_or_create(name='Admin')
        Group.objects.get_or_create(name='Agent')
        Group.objects.get_or_create(name='Client')