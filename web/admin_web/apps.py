from django.apps import AppConfig
from django.contrib.auth import get_user_model
from django.db import ProgrammingError

from web.config import web_settings


class AdminWebConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'admin_web'

    def ready(self):
        user_model = get_user_model()

        try:
            user_model.objects.get(username=web_settings.ADMIN_USER)
        except user_model.DoesNotExist:
            user_model.objects.create_superuser(
                web_settings.ADMIN_USER, f'test@admin-panel.com', web_settings.ADMIN_PASSWORD
            )
        except ProgrammingError:
            pass
