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
from database import db_manager, repo
from database.base_repository import BaseRepository
from database.models import SessionPersonal, Session, PersonalSex


class SessionPersonalRepository(BaseRepository):
    @db_manager
    def get_sex(self, session: Session) -> PersonalSex:
        sps = self.get_all(session=session)
        for sp in sps:
            personal = repo.personals.get(sp.personal_id)
            if personal.sex == PersonalSex.unisex:
                continue
            return personal.sex


sessions_personals = SessionPersonalRepository(SessionPersonal)
