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


from peewee import PrimaryKeyField, ForeignKeyField, CharField, TextField

from database.db import BaseModel
from . import Session, Group, Order, Message, User


class SessionTaskType:
    non_type = 'non_type'
    join_group = 'join_group'
    send_by_order = 'send_by_order'
    send_by_mailing = 'send_by_mailing'
    check_message = 'check_message'
    check_spamblock = 'check_spamblock'
    change_fi = 'change_fi'
    change_avatar = 'change_avatar'


class SessionTaskStates:
    enable = 'enable'
    finished = 'finished'
    abortively = 'abortively'


class SessionTask(BaseModel):
    id = PrimaryKeyField()
    session = ForeignKeyField(Session, to_field='id', null=True)
    user = ForeignKeyField(User, to_field='id', null=True)
    group = ForeignKeyField(Group, to_field='id', null=True)
    order = ForeignKeyField(Order, to_field='id', null=True)
    message = ForeignKeyField(Message, to_field='id', null=True)

    type = CharField(max_length=32, default=SessionTaskType.non_type)
    state = CharField(max_length=32, default=SessionTaskStates.enable)
    state_description = TextField(null=True)

    class Meta:
        db_table = 'sessions_tasks'
