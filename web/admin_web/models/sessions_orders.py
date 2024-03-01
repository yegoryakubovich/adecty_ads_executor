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

from admin_web.models import Session, Order


class SessionOrder(models.Model):
    class Meta:
        db_table = 'sessions_orders'
        verbose_name = 'Сессия-Заказ'
        verbose_name_plural = 'Сессии-Заказы'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.utcnow, verbose_name="Время создания")

    session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name="Сессия",
                                related_name="sessions_orders_session")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ",
                              related_name="sessions_orders_order")

    def __str__(self):
        return f"{self.session}"
