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
from random import choice

from core.constants import avatar_path
from core.default_data import names_man, names_woman, surnames_man, surnames_woman, avatars_man, avatars_woman, \
    avatars_unisex, about_unisex
from database import db_manager
from database.base_repository import BaseRepository
from database.models import Personal, PersonalTypes, PersonalSex


class PersonalRepository(BaseRepository):

    @db_manager
    def fill(self):
        for name in names_man:
            self.create(type=PersonalTypes.name, value=name, sex=PersonalSex.man)
        for name in names_woman:
            self.create(type=PersonalTypes.name, value=name, sex=PersonalSex.woman)

        for surname in surnames_man:
            self.create(type=PersonalTypes.surname, value=surname, sex=PersonalSex.man)
        for surname in surnames_woman:
            self.create(type=PersonalTypes.surname, value=surname, sex=PersonalSex.woman)

        for avatar_name in avatars_man:
            self.create(type=PersonalTypes.avatar, value=f"{avatar_path}{avatar_name}", sex=PersonalSex.man)
        for avatar_name in avatars_woman:
            self.create(type=PersonalTypes.avatar, value=f"{avatar_path}{avatar_name}", sex=PersonalSex.woman)
        for avatar_name in avatars_unisex:
            self.create(type=PersonalTypes.avatar, value=f"{avatar_path}{avatar_name}", sex=PersonalSex.unisex)

        for about in about_unisex:
            self.create(type=PersonalTypes.about, value=about, sex=PersonalSex.unisex)

    @db_manager
    def get_random(self, p_type: PersonalTypes, sex: PersonalSex):
        result = [item for item in self.get_all(type=p_type, sex=PersonalSex.unisex)]
        result.extend([item for item in self.get_all(type=p_type, sex=sex)])
        return choice(result) if result else None


personals = PersonalRepository(Personal)
