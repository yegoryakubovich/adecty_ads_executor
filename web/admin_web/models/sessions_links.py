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


from datetime import datetime

from django.db import models

from admin_web.models import Session


class SessionLink(models.Model):
    class Meta:
        db_table = 'sessions_links'
        verbose_name = 'Сессия-Сессия'
        verbose_name_plural = 'Сессии-Сессии'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    session_1 = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name="sessions_links_session_1", verbose_name="Сессия 1")
    session_2 = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name="sessions_links_session_2", verbose_name="Сессия 2")
