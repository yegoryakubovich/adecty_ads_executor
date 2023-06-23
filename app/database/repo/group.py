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
from typing import List

from core.constants import groups_list
from database import db_manager
from database.models import Group, GroupStates

model = Group


class GroupRepository:
    def __init__(self):
        self.model = model

    @db_manager
    def add_new_group(self, ):
        for item in groups_list:
            if item.count("@"):
                item = item[1:]
            self.model.get_or_create(name=item)

    @db_manager
    def get_by_id(self, id: int) -> model:
        return self.model.get_or_none(id=id)

    @db_manager
    def get_all_by_state(self, state: GroupStates) -> List[model]:
        return self.model.select().filter(state=state).execute()


groups = GroupRepository()
