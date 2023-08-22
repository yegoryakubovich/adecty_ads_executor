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

from admin_web.models import Session, Personal, PersonalTypes


class SessionPersonal(models.Model):
    class Meta:
        db_table = 'sessions_personals'
        verbose_name = 'Связь персонали'
        verbose_name_plural = 'Связи персоналей'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Сессия",
                                related_name="sessions_personals_session")
    personal = models.ForeignKey(Personal, on_delete=models.CASCADE, verbose_name="Персональ",
                                 related_name="sessions_personals_personals")

    type = models.CharField(max_length=64, choices=PersonalTypes.choices, verbose_name="Тип")

    def __str__(self):
        return f"{self.session}-{self.personal} ({self.id})"
