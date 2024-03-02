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


class OurGroupStates:
    active = 'active'
    inactive = 'inactive'

    choices = ((active, active), (inactive, inactive))


class OurGroup(models.Model):
    class Meta:
        db_table = 'ours_groups'
        verbose_name = 'Наша группа'
        verbose_name_plural = 'Наши группы'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    name = models.CharField(max_length=128, unique=True, verbose_name="Название")
    state = models.CharField(max_length=32, choices=OurGroupStates.choices, verbose_name="Состояние")

    def __str__(self):
        return f"{self.id} - {self.name}  ({self.state})"

