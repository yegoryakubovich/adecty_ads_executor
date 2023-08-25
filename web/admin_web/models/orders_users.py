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

from admin_web.models import Order, User


class OrderUserStates:
    active = 'active'
    abort = 'abort'
    finish = 'finish'

    choices = ((active, active), (abort, abort), (finish, finish))


class OrderUser(models.Model):
    class Meta:
        db_table = 'orders_users'
        verbose_name = 'Заказ-Пользователь'
        verbose_name_plural = 'Заказы-Пользователи'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="orders_users_session", verbose_name="Пользователь")
    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name="orders_users_order", verbose_name="Заказ")

    state = models.CharField(max_length=64, choices=OrderUserStates.choices, verbose_name="Состояние")
    state_description = models.CharField(max_length=64, null=True, blank=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.id}"
