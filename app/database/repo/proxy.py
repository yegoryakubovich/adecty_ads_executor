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

from random import randint
from typing import List

from core.constants import proxies_list
from database import db_manager, repo
from database.models import Proxy, ProxyTypes, ProxyStates

model = Proxy


class ProxyRepository:
    def __init__(self):
        self.model = model

    @db_manager
    def add_new_proxy(self, ):
        for item in proxies_list:
            item_data = item.split("@")
            self.model.get_or_create(
                type=ProxyTypes.socks5, host=item_data[1].split(':')[0], port=item_data[1].split(':')[1],
                user=item_data[0].split(':')[0], password=item_data[0].split(':')[1],
                country=repo.countries.get_by_id(1)
            )

    @db_manager
    def get_count(self) -> int:
        return self.model.select().count()

    @db_manager
    def get_by_id(self, id: int) -> model:
        return self.model.get_or_none(id=id)

    @db_manager
    def get(self, **kwargs) -> model:
        return self.model.get_or_none(**kwargs)

    @db_manager
    def get_all_by_state(self, state: ProxyStates) -> List[model]:
        return self.model.select().filter(state=state).execute()

    @db_manager
    def get_all(self) -> List[model]:
        return self.model.select().execute()

    @db_manager
    def update(self, proxy: Proxy, **kwargs) -> model:
        return self.model.update(**kwargs).where(self.model.id == proxy.id).execute()

    @db_manager
    def get_dict(self, proxy_id: int) -> dict:
        proxy = self.get_by_id(proxy_id)
        return {
            "scheme": proxy.type,
            "hostname": proxy.host, "port": proxy.port,
            "username": proxy.user, "password": proxy.password
        }

    @db_manager
    def get_random_dict(self):
        return self.get_dict(randint(1, self.get_count()))


proxies = ProxyRepository()
