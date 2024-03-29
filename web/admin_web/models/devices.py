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


class Device(models.Model):
    class Meta:
        db_table = 'devices'
        verbose_name = 'Устройство'
        verbose_name_plural = 'Устройства'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    system_version = models.CharField(max_length=128, verbose_name="Версия системы")
    device_model = models.CharField(max_length=128, verbose_name="Модель устройства")

    def __str__(self):
        return f"{self.id} {self.system_version} {self.device_model}"
