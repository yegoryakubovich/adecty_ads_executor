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
from database.models import SessionStates


async def check_banned(client):
    async with client:
        try:
            await client.get_chat('durov')
            return True
        except:
            return False


async def check_wait_sessions():
    for session in repo.sessions.get_all_by_state(state=SessionStates.wait):
        client = await session_actions.open_session(session)
        if await check_banned(client):
            repo.sessions.move_state(session, SessionStates.free)
        else:
            repo.sessions.move_state(session, SessionStates.banned)


# async def check_free_sessions():
#     for session in repo.sessions.get_all_by_state(state=SessionStates.free):
#         client = await session_actions.open_session(session)
#         if await check_banned(client):
#             repo.sessions.move_state(session, SessionStates.free)
#         else:
#             repo.sessions.move_state(session, SessionStates.banned)
