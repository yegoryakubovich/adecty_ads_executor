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


from datetime import datetime, timedelta

from pyrogram import Client

from database import repo
from database.models import Session, SessionTaskType, SessionTaskStates, OurGroupStates
from functions.bot.executor import BotExecutorAction


class SimulatorAction:
    def __init__(self, client: Client, session: Session, executor: BotExecutorAction):
        self.client = client
        self.session = session
        self.executor = executor
        self.next_data: datetime = datetime.utcnow()

    def run(self):
        date_now = datetime.utcnow()
        if self.next_data > date_now:
            return
        # update session data
        self.session = repo.sessions.get(id=self.session.id)
        # read history
        await self.executor.read_all_chat_history()
        # check our group follower
        our_group = repo.ours_groups.get_by(state=OurGroupStates.active)
        session_our_group = repo.sessions_ours_groups.get_by(session=self.session, our_group=our_group)
        if not session_our_group:
            if repo.sessions_tasks.get_by(
                    session=self.session,
                    our_group=our_group,
                    type=SessionTaskType.join_group,
                    state=SessionTaskStates.enable,
            ):
                return
            # create task join group
            repo.sessions_tasks.create(
                session=self.session,
                our_group=our_group,
                type=SessionTaskType.join_group,
                state=SessionTaskStates.enable,
            )
        # add contact
        contacts_count = repo.sessions_links.get_contacts_count()
        if contacts_count < self.session.grade.contact_max:  # check contact limits
            chat_members = await self.executor.get_our_group_members(our_group=our_group, limit=1)
            for chat_member in chat_members:
                await self.executor.add_contact(chat_member=chat_member)
        # send message to mutual contact
        for session_link in repo.sessions_links.get_all(session_1=self.session):
            mutual = repo.sessions_links.get_by(session_1=session_link.session_2, session_2=session_link.session_1)
            if not mutual:
                continue
            dialog_message = repo.dialogs_messages.get_random()
            await self.executor.send_message(chat_id=session_link.session_2.tg_user_id, text=dialog_message.message)
        # sleep
        sleep = int(repo.settings.get_by(key="simulator_sleep").value)
        self.next_data = date_now + timedelta(seconds=sleep)
