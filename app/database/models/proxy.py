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

from peewee import PrimaryKeyField, IntegerField, CharField, ForeignKeyField, DateTimeField

from . import Shop
from .base import BaseModel
from .country import Country


class ProxyTypes:
    http = "http"
    socks5 = "socks5"


class ProxyStates:
    wait = "wait"
    enable = "enable"
    disable = "disable"


class Proxy(BaseModel):
    id = PrimaryKeyField()
    type = CharField(max_length=128)
    country = ForeignKeyField(Country, to_field='id')
    shop = ForeignKeyField(Shop, to_field='id')
    host = CharField(max_length=32)
    port = IntegerField()
    user = CharField(max_length=128)
    password = CharField(max_length=256)

    state = CharField(max_length=64, default=ProxyStates.wait)
    state_description = CharField(max_length=2056, null=True)
    created = DateTimeField(default=datetime.utcnow)

    class Meta:
        db_table = 'proxies'
