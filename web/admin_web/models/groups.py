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


class GroupStates:
    waiting = 'waiting'
    active = 'active'
    inactive = 'inactive'

    choices = ((waiting, waiting), (active, active), (inactive, inactive))


class GroupType:
    link = 'link'
    no_link = 'no_link'
    short = 'short'
    replace = 'replace'
    inactive = 'inactive'

    choices = ((link, link), (no_link, no_link), (short, short), (replace, replace), (inactive, inactive))


class GroupCaptionType:
    join_group = "join_group"
    click_button = "click_button"
    other = "other"

    choices = ((join_group, join_group), (click_button, click_button), (other, other),)


class Group(models.Model):
    class Meta:
        db_table = 'groups'
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    name = models.CharField(max_length=128, unique=True, verbose_name="Название")
    state = models.CharField(max_length=32, default=GroupStates.waiting, choices=GroupStates.choices,
                             verbose_name="Состояние")
    subscribers = models.IntegerField(verbose_name="Подписчиков")  # Количество подписчиков

    can_image = models.BooleanField(default=True, verbose_name="Картинки")
    type = models.CharField(max_length=32, default=GroupType.link, choices=GroupType.choices, verbose_name="Тип")
    join_request = models.BooleanField(default=False, verbose_name="Запрос вступления")
    captcha_have = models.BooleanField(default=False, verbose_name="Капча")
    captcha_type = models.CharField(max_length=128, null=True, blank=True, choices=GroupCaptionType.choices,
                                    verbose_name="Тип капчи")
    captcha_data = models.CharField(max_length=128, null=True, blank=True, verbose_name="Информация капчи")

    def __str__(self):
        return f"{self.id} - {self.name}  ({self.state})"
