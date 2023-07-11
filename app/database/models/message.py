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

from peewee import PrimaryKeyField, CharField, ForeignKeyField, DateTimeField, BigIntegerField

from database.db import BaseModel
from . import Group, Order
from .session import Session


class MessageStates:
    waiting = 'waiting'
    fine = 'fine'
    deleted = 'deleted'


class Message(BaseModel):
    id = PrimaryKeyField()
    session = ForeignKeyField(Session, to_field='id')
    order = ForeignKeyField(Order, to_field='id', null=True)
    group = ForeignKeyField(Group, to_field='id')
    state = CharField(max_length=64, default=MessageStates.waiting)

    message_id = BigIntegerField()
    text = CharField(max_length=1024, null=True)

    class Meta:
        db_table = 'messages'
