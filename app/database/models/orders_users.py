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
from peewee import PrimaryKeyField, ForeignKeyField, CharField

from database.db import BaseModel
from . import Order, User


class OrderUserStates:
    active = 'active'
    abort = 'abort'
    finish = 'finish'


class OrderUser(BaseModel):
    id = PrimaryKeyField()
    user = ForeignKeyField(User, to_field='id')
    order = ForeignKeyField(Order, to_field='id')

    state = CharField(max_length=64, default=OrderUserStates.active)
    state_description = CharField(max_length=64, null=True)

    class Meta:
        db_table = 'orders_users'
