#
# (c) 2023, Yegor Yakubovich, yegoryakubovich.com, personal@yegoryakybovich.com
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
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
