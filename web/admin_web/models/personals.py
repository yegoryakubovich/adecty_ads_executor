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


class PersonalTypes:
    name = 'name'
    surname = 'surname'
    avatar = 'avatar'
    about = 'about'

    choices = ((name, name), (surname, surname), (avatar, avatar), (about, about))


class PersonalSex:
    man = 'man'
    woman = 'woman'
    unisex = 'unisex'

    choices = ((man, man), (woman, woman), (unisex, unisex))


class Personal(models.Model):
    class Meta:
        db_table = 'personals'
        verbose_name = 'Персонал'
        verbose_name_plural = 'Персонали'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    type = models.CharField(max_length=64, choices=PersonalTypes.choices, verbose_name="Тип")
    value = models.CharField(max_length=256, verbose_name="Значение")
    sex = models.CharField(max_length=256, choices=PersonalSex.choices, verbose_name="Пол")

    def __str__(self):
        return f"{self.id} ({self.type}) - {self.value}"
