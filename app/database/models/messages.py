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


from peewee import PrimaryKeyField, CharField, ForeignKeyField, BigIntegerField

from database.db import BaseModel
from . import Group, Order, User
from .sessions import Session


class MessageStates:
    from_spam = 'from_spam'
    to_spam = 'to_spam'
    from_user = 'from_user'
    to_user = 'to_user'
    waiting = 'waiting'
    fine = 'fine'
    deleted = 'deleted'


class Message(BaseModel):
    id = PrimaryKeyField()
    session = ForeignKeyField(Session, to_field='id', null=True)
    user = ForeignKeyField(User, to_field='id', null=True)
    order = ForeignKeyField(Order, to_field='id', null=True)
    group = ForeignKeyField(Group, to_field='id', null=True)

    message_id = BigIntegerField()
    text = CharField(max_length=1024, null=True)

    state = CharField(max_length=64, default=MessageStates.waiting)

    class Meta:
        db_table = 'messages'
