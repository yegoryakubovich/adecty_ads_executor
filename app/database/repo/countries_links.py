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
from database.models import CountryLink, Country


class CountryLinkRepository(BaseRepository):

    @db_manager
    def get_link_country(self, country: Country):
        ids = [country.id]
        ids += [c.country_2_id for c in self.get_all(country_1=country)]
        ids += [c.country_1_id for c in self.get_all(country_2=country)]
        return [repo.countries.get(c_id) for c_id in list(set(ids))]


countries_links = CountryLinkRepository(CountryLink)
