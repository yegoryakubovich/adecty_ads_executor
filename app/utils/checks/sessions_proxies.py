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
from database import repo
from database.models import Session


async def find_new_link(session: Session):
    return repo.sessions_proxies.create(session=session, proxy=repo.sessions_proxies.get_free_proxy())[0]

# async def check_link_sessions():
#     for session in repo.sessions.get_all_enable():
#         client = await session_actions.open_session(session)
#         async with client:
#             try:
#                 await client.get_entity('durov')
#                 if session.id == 1:
#                     raise UserDeactivatedBanError
#             except (UserDeactivatedBanError, UnauthorizedError):
#                 repo.sessions.move_state(SessionStates.banned)
