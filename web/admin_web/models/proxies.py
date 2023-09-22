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


class ProxyTypes:
    http = "http"
    socks5 = "socks5"

    choices = ((http, http), (socks5, socks5))


class ProxyStates:
    wait = "wait"
    enable = "enable"
    disable = "disable"
    stop = "stop"

    choices = ((wait, wait), (enable, enable), (disable, disable), (stop, stop))


class Proxy(models.Model):
    class Meta:
        db_table = 'proxies'
        verbose_name = 'Прокси'
        verbose_name_plural = 'Прокси'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    type = models.CharField(max_length=128, choices=ProxyTypes.choices, verbose_name="Тип")
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, verbose_name="Страна")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name="Магазин")
    host = models.CharField(max_length=32, verbose_name="Host")
    port = models.IntegerField(verbose_name="Port")
    user = models.CharField(max_length=128, verbose_name="User")
    password = models.CharField(max_length=256, verbose_name="Password")
    max_link = models.IntegerField(default=3, verbose_name="Максимум подключений")

    state = models.CharField(max_length=64, default=ProxyStates.wait, choices=ProxyStates.choices,
                             verbose_name="Состояние")
    state_description = models.CharField(max_length=2056, null=True, blank=True, verbose_name="Описание состояния")

    def __str__(self):
        return f"{self.id} ({self.state})"
