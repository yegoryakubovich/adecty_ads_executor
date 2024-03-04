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


class Grade(models.Model):
    class Meta:
        db_table = 'grades'
        verbose_name = 'Уровень сессий'
        verbose_name_plural = 'Уровни сессий'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name='Время создания')

    level = models.IntegerField(unique=True, null=False, verbose_name='Уровень')
    message_day = models.BigIntegerField(default=0, verbose_name='Сообщений в день')
    check_message_max = models.BigIntegerField(default=0, verbose_name='Проверок сообщений (макс)')
    contact_max = models.BigIntegerField(default=0, verbose_name='Контактов (макс)')
    active_group_max = models.BigIntegerField(default=0, verbose_name='Активных групп (макс)')

    def __str__(self):
        return f'{self.id} - {self.level}'
