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

from database import db_manager
from database.base_repository import BaseRepository
from database.models import Proxy

model = Proxy


class ProxyRepository(BaseRepository):

    @db_manager
    def get_dict(self, proxy_id: int) -> dict:
        proxy = self.get(proxy_id)
        return {
            "scheme": proxy.type,
            "hostname": proxy.host, "port": proxy.port,
            "username": proxy.user, "password": proxy.password
        }

    @db_manager
    def get_random_dict(self):
        return self.get_dict(randint(1, self.count()))


proxies = ProxyRepository(Proxy)
