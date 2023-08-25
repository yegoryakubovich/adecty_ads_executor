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

from admin_web.models import Session, Group, Order, Message, User


class SessionTaskType:
    check_group = 'check_group'
    join_group = 'join_group'
    send_by_order = 'send_by_order'
    send_by_mailing = 'send_by_mailing'
    check_message = 'check_message'
    change_fi = 'change_fi'
    change_avatar = 'change_avatar'

    choices = (
        (check_group, check_group), (join_group, join_group), (check_message, check_message),
        (send_by_order, send_by_order), (send_by_mailing, send_by_mailing),
        (change_fi, change_fi), (change_avatar, change_avatar)
    )


class SessionTaskStates:
    enable = 'enable'
    finished = 'finished'
    abortively = 'abortively'

    choices = ((enable, enable), (finished, finished), (abortively, abortively))


class SessionTask(models.Model):
    class Meta:
        db_table = 'sessions_tasks'
        verbose_name = 'Задача сессии'
        verbose_name_plural = 'Задачи сессий'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True,
                                related_name="session_tasks_session", verbose_name="Сессия")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,
                             related_name="session_tasks_user", verbose_name="Пользователь")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True,
                              related_name="session_tasks_group", verbose_name="Группа")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True,
                              related_name="session_tasks_order", verbose_name="Заказ")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, null=True, blank=True,
                                related_name="session_tasks_message", verbose_name="Сообщение")

    type = models.CharField(max_length=32, choices=SessionTaskType.choices, verbose_name="Тип")
    state = models.CharField(max_length=32, default=SessionTaskStates.enable, choices=SessionTaskStates.choices,
                             verbose_name="Состояние")
    state_description = models.CharField(max_length=64, null=True, blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.id} ({self.state})"
