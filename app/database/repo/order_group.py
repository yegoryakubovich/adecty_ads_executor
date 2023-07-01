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

from database import db_manager
from database.models import OrderGroup, Order

model = OrderGroup


class OrderGroupRepository:
    def __init__(self):
        self.model = model

    @db_manager
    def create(self, **kwargs):
        return self.model.get_or_create(**kwargs)

    @db_manager
    def get_count(self) -> int:
        return self.model.select().count()

    @db_manager
    def get_by_id(self, id: int) -> model:
        return self.model.get_or_none(id=id)

    @db_manager
    def get_all(self) -> List[model]:
        return self.model.select().execute()

    @db_manager
    def get_by_order(self, order: Order) -> List[model]:
        return self.model.select().where(self.model.order == order).execute()


orders_groups = OrderGroupRepository()
