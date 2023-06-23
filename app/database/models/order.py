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
from peewee import PrimaryKeyField, CharField, DateTimeField

from database.db import BaseModel


class OrderStates:
    wait = "wait"
    enable = "enable"
    disable = "disable"


class Order(BaseModel):
    id = PrimaryKeyField()
    name = CharField(max_length=128)
    message = CharField(max_length=256)

    state = CharField(max_length=32, default=OrderStates.wait)
    datetime_stop = DateTimeField()

    class Meta:
        db_table = 'orders'
