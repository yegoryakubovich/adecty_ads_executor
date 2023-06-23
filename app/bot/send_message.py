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
from bot.sessions import session_actions
from database import repo
from database.models import Order, GroupStates


async def smart_send_message(order: Order):
    for group in repo.groups.get_all_by_state(state=GroupStates.active):
        session_from_send_msg = repo.messages.get_session_from_send_message(order=order, group=group)
        client = await session_actions.open_session(session_from_send_msg)
        await session_actions.send_message(client, group.name, order.message)
