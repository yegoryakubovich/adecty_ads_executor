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
from database.models import Group


class GroupRepository(BaseRepository):

    @db_manager
    def fill(self):
        for item in groups_list:
            if item.count("@"):
                item = item[1:]
            self.model.get_or_create(name=item)


groups = GroupRepository(Group)
