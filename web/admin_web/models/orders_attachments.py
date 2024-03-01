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

from admin_web.models import Order


class OrderAttachmentTypes:
    image_common = 'image_common'
    text_common = 'text_common'
    text_no_link = 'text_no_link'
    text_short = 'text_short'
    text_replace = 'text_replace'
    text_answer = 'text_answer'

    choices = (
        (image_common, image_common), (text_common, text_common), (text_no_link, text_no_link),
        (text_short, text_short), (text_replace, text_replace), (text_answer, text_answer)
    )


class OrderAttachment(models.Model):
    class Meta:
        db_table = 'orders_attachments'
        verbose_name = 'Заказ-Вложение'
        verbose_name_plural = 'Заказы-Вложения'

    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(default=datetime.now, verbose_name="Время создания")

    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name="orders_attachments_order", verbose_name="Заказ")
    type = models.CharField(max_length=64, choices=OrderAttachmentTypes.choices, verbose_name="Тип")
    value = models.TextField(verbose_name="Значение")

    def __str__(self):
        return f"{self.id}"
