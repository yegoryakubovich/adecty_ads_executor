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


class User(models.Model):
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    phone = models.BigIntegerField(null=True, verbose_name="Номер")
    tg_user_id = models.BigIntegerField(null=True, verbose_name="Telegram ID")
    username = models.CharField(max_length=32, null=True, verbose_name="Username")
    first_name = models.CharField(max_length=32, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=32, null=True, verbose_name="Фамилия")

    def __str__(self):
        return f"{self.id} ({self.username})"
