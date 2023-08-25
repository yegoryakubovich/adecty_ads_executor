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
from core.default_data import groups_list
from database import db_manager
from database.base_repository import BaseRepository
from database.models import Group, GroupType


class GroupRepository(BaseRepository):

    @db_manager
    def fill(self):
        for item in groups_list:
            if item.count("@"):
                item = item[1:]
            self.model.get_or_create(name=item)

    @db_manager
    def update_to_next_type(self, group: Group):
        g_type = None
        if group.type == GroupType.link:
            g_type = GroupType.no_link
        elif group.type == GroupType.no_link:
            g_type = GroupType.short
        elif group.type == GroupType.short:
            g_type = GroupType.replace
        elif group.type == GroupType.replace:
            g_type = GroupType.inactive

        if g_type:
            self.update(group, type=g_type)



groups = GroupRepository(Group)
