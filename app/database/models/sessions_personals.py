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
from . import Personal, Session


class SessionPersonal(BaseModel):
    id = PrimaryKeyField()

    session = ForeignKeyField(Session, to_field='id')
    personal = ForeignKeyField(Personal, to_field='id')

    type = CharField(max_length=64)

    class Meta:
        db_table = 'sessions_personals'
