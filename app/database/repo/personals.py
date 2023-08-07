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

from core.default_data import surname_data, names_data
from database import db_manager
from database.base_repository import BaseRepository
from database.models import Personal
from database.models.personal import PersonalTypes


class PersonalRepository(BaseRepository):

    @db_manager
    def fill(self):
        for name in names_data:
            self.create(type=PersonalTypes.name, value=name)

        for surname in surname_data:
            self.create(type=PersonalTypes.surname, value=surname)

        self.create(type=PersonalTypes.about, value="TG: @fexps_obmen")
        self.create(type=PersonalTypes.avatar, value="media/bot/avatars/pBIZFD8NqDg.jpg")

    @db_manager
    def get_random_pack(self):
        names = [item for item in self.get_all(type=PersonalTypes.name)]
        name = choice(names).value if names else None
        surnames = [item for item in self.get_all(type=PersonalTypes.surname)]
        surname = choice(surnames).value if surnames else None
        abouts = [item for item in self.get_all(type=PersonalTypes.about)]
        about = choice(abouts).value if abouts else None
        avatars = [item for item in self.get_all(type=PersonalTypes.avatar)]
        avatar = choice(avatars).value if avatars else None

        return name, surname, about, avatar


personals = PersonalRepository(Personal)
