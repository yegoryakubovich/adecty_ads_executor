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

from admin_web.models import Session, Group


class SessionGroupState:
    active = 'active'
    banned = 'banned'

    choices = ((active, active), (banned, banned))


class SessionGroup(models.Model):
    class Meta:
        db_table = 'sessions_groups'
        verbose_name = 'Сессия-Группа'
        verbose_name_plural = 'Сессии-Группы'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    session = models.ForeignKey(Session, on_delete=models.CASCADE,
                                related_name="session_group_session", verbose_name="Сессия")
    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name="session_group_group", verbose_name="Группа")
    state = models.CharField(max_length=64, choices=SessionGroupState.choices, verbose_name="Состояние")

    def __str__(self):
        return f"{self.session}-{self.group} ({self.state})"
