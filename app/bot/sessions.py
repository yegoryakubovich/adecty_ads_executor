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
from pyrogram import Client

from database import repo
from database.models import Session, SessionProxy
from utils.checks.sessions_proxies import find_new_link


class SessionActions:
    async def open_session(self, session: Session) -> Client:
        sp: SessionProxy = repo.sessions_proxies.get_by_session(session=session)
        if not sp:
            sp = await find_new_link(session)
        return Client(
            f"{session.id}", session_string=session.string, api_id=session.api_id, api_hash=session.api_hash,
            proxy=repo.proxies.get_dict(proxy_id=sp.proxy_id)
        )

    async def send_message(self, client: Client, chat_id: str, text: str):
        await client.start()
        await client.join_chat(chat_id)
        await client.send_message(chat_id, text)
        await client.stop()


session_actions = SessionActions()
