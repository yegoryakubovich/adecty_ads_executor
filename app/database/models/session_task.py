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

from . import Session, Group, Order, Message
from .base import BaseModel


class SessionTaskType:
    non_type = 'non_type'
    check_group = 'check_group'
    join_group = 'join_group'
    send_by_order = 'send_by_order'
    check_message = 'check_message'


class SessionTaskStates:
    enable = 'enable'
    finished = 'finished'
    abortively = 'abortively'


class SessionTask(BaseModel):
    id = PrimaryKeyField()
    session = ForeignKeyField(Session, to_field='id')
    group = ForeignKeyField(Group, to_field='id', null=True)
    order = ForeignKeyField(Order, to_field='id', null=True)
    message = ForeignKeyField(Message, to_field='id', null=True)

    state = CharField(max_length=32, default=SessionTaskStates.enable)
    type = CharField(max_length=32, default=SessionTaskType.non_type)

    class Meta:
        db_table = 'sessions_tasks'
