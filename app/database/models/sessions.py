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
from peewee import PrimaryKeyField, BigIntegerField, CharField, ForeignKeyField, IntegerField, BooleanField

from database.db import BaseModel
from . import Shop
from .country import Country


class SessionStates:
    waiting = "waiting"
    check = "check"
    free = "free"
    in_work = "in_work"
    banned = "banned"
    spam_block = "spam_block"


class Session(BaseModel):
    id = PrimaryKeyField()
    phone = BigIntegerField()
    country = ForeignKeyField(Country, to_field='id')
    shop = ForeignKeyField(Shop, to_field='id')

    string = CharField(max_length=512)
    api_id = BigIntegerField()
    api_hash = CharField(max_length=256)

    tg_user_id = BigIntegerField()
    username = CharField(max_length=128, null=True)
    first_name = CharField(max_length=128, null=True)
    last_name = CharField(max_length=128, null=True)

    state = CharField(max_length=64, default=SessionStates.waiting)
    state_description = CharField(max_length=2056, null=True)
    work = BooleanField(default=False)
    messages_send = IntegerField()

    class Meta:
        db_table = 'sessions'