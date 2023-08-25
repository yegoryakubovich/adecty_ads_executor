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

from admin_web.models import Country, Shop


class SessionStates:
    waiting = "waiting"
    check = "check"
    free = "free"
    in_work = "in_work"
    banned = "banned"
    spam_block = "spam_block"

    choices = (
        (waiting, waiting), (check, check), (free, free), (in_work, in_work), (banned, banned), (spam_block, spam_block)
    )


class Session(models.Model):
    class Meta:
        db_table = 'sessions'
        verbose_name = 'Сессия'
        verbose_name_plural = 'Сессии'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    phone = models.BigIntegerField(verbose_name="Номер")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, verbose_name="Страна")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Магазин")

    string = models.CharField(max_length=512, verbose_name="String session")
    api_id = models.BigIntegerField(verbose_name="API ID")
    api_hash = models.CharField(max_length=256, verbose_name="API HASH")

    tg_user_id = models.BigIntegerField(verbose_name="Телеграм ID")
    username = models.CharField(max_length=128, null=True, blank=True, verbose_name="USERNAME")

    state = models.CharField(max_length=64, default=SessionStates.waiting, choices=SessionStates.choices,
                             verbose_name="Состояние")
    work = models.BooleanField(default=False, verbose_name="Запущен")

    def __str__(self):
        return f"{self.id} ({self.state})"
