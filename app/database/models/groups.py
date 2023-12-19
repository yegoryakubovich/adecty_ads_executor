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
from peewee import PrimaryKeyField, CharField, IntegerField, BooleanField

from database.db import BaseModel


class GroupStates:
    waiting = 'waiting'
    active = 'active'
    inactive = 'inactive'


class GroupType:
    link = 'link'
    no_link = 'no_link'
    short = 'short'
    replace = 'replace'
    inactive = 'inactive'


class GroupCaptionType:
    join_group = "join_group"
    click_button = "click_button"
    other = "other"


class Group(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=128)
    state = CharField(max_length=32, default=GroupStates.waiting)
    subscribers = IntegerField()  # Количество подписчиков

    can_image = BooleanField(default=True)  # Отправка с картинками
    type = CharField(max_length=32, default=GroupType.link, null=True)  # Отправка ссылок
    join_request = BooleanField(default=False)
    captcha_have = BooleanField(default=False)
    captcha_type = CharField(max_length=128, null=True)
    captcha_data = CharField(max_length=128, null=True)

    class Meta:
        db_table = 'groups'
