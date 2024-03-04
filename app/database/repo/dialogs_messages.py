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
import random

from database import db_manager
from database.base_repository import BaseRepository
from database.models import DialogMessage


class DialogMessageRepository(BaseRepository):
    model = DialogMessage

    @db_manager
    def get_random(self) -> DialogMessage:
        return random.choice(self.get_all())


dialogs_messages = DialogMessageRepository(DialogMessage)
