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

from admin_web.models import Session, User, Order, Group


class MessageStates:
    from_spam = 'from_spam'
    to_spam = 'to_spam'
    from_user = 'from_user'
    to_user = 'to_user'
    waiting = 'waiting'
    fine = 'fine'
    deleted = 'deleted'

    choices = (
        (from_spam, from_spam), (to_spam, to_spam),
        (from_user, from_user), (to_user, to_user),
        (waiting, waiting), (fine, fine), (deleted, deleted)
    )


class Message(models.Model):
    class Meta:
        db_table = 'messages'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True,
                                related_name="message_session", verbose_name="Сессия")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="message_user",
                             verbose_name="Пользователь")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True, related_name="message_order",
                              verbose_name="Заказ")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name="message_group",
                              verbose_name="Группа")
    state = models.CharField(max_length=64, default=MessageStates.waiting, choices=MessageStates.choices,
                             verbose_name="Состояние")

    message_id = models.BigIntegerField(blank=True, verbose_name="ID Сообщения")
    text = models.CharField(max_length=1024, null=True, verbose_name="Текст")

    def __str__(self):
        return f"{self.id} ({self.state})"
