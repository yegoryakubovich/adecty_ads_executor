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

from admin_web.models import Country, Group


class GroupCountry(models.Model):
    class Meta:
        db_table = 'groups_countries'
        verbose_name = 'Группа-Страна'
        verbose_name_plural = 'Группы-Страны'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    group = models.ForeignKey(Group, on_delete=models.CASCADE,
                              related_name="groups_countries_group", verbose_name="Группа")
    country = models.ForeignKey(Country, on_delete=models.CASCADE,
                                related_name="groups_countries_country", verbose_name="Страна 1")
