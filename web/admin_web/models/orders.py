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
from datetime import datetime

from django.db import models


class OrderStates:
    waiting = "waiting"
    disable = "finished"
    stopped = "stopped"

    choices = ((waiting, waiting), (disable, disable), (stopped, stopped))


class OrderTypes:
    ads = "ads"
    mailing = "mailing"

    choices = ((ads, ads), (mailing, mailing))


class Order(models.Model):
    class Meta:
        db_table = 'orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    name = models.CharField(max_length=128, verbose_name="Название")
    message = models.TextField(verbose_name="Сообщение")
    message_no_link = models.TextField(null=True, blank=True, verbose_name="Сообщение без ссылки")
    message_short = models.TextField(null=True, blank=True, verbose_name="Сообщение короткое")
    image_link = models.CharField(max_length=256, null=True, blank=True, verbose_name="Ссылка на картинку")

    state = models.CharField(max_length=32, default=OrderStates.waiting, choices=OrderStates.choices,
                             verbose_name="Состояние")
    type = models.CharField(max_length=32, null=True, blank=True, choices=OrderTypes.choices, verbose_name="Тип")

    datetime_stop = models.DateTimeField()

    def __str__(self):
        return f"{self.id} - {self.name} ({self.state})"
