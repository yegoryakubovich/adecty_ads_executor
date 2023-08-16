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
from django import forms

from admin_web.models import Order, OrderTypes


class AddUsersForm(forms.Form):
    users = forms.CharField(widget=forms.Textarea, label="Пользователи через запятую", required=True)


class MailingUsersForm(forms.Form):
    choices = [(order.id, f"{order.id} - {order.name}") for order in Order.objects.filter(type=OrderTypes.mailing).all()]
    order = forms.ChoiceField(choices=choices, label="Выбор ордера", required=True)