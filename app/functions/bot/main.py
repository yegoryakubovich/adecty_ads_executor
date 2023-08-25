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
import asyncio
from typing import Optional

from loguru import logger
from pyrogram import Client, errors, enums

from core.constants import ASSISTANT_SLEEP_SEC, ANSWER_MESSAGE
from database import repo
from database.models import Session, SessionProxy, SessionStates, MessageStates, User, SessionTaskType, \
    SessionTaskStates
from functions.bot.executor import BotExecutorAction
from functions.bot.simulator import SimulatorAction
from functions.bot.tasker import BotTaskerAction
from utils.decorators import func_logger
from utils.helpers import smart_sleep, smart_create_sleep


class BotAction:
    client = None
    executor = None
    simulator = None
    tasker = None

    def __init__(self, session: Session):
        self.session = session
        self.black_list = [session.id, 777000]
        self.prefix = f"Session #{self.session.id}"

    async def open_session(self) -> Optional[Client]:
        sp: SessionProxy = repo.sessions_proxies.get_by_session(session=self.session)
        if not sp:
            self.logger("No find proxy")
            return
        return Client(
            f"{self.session.id}", session_string=self.session.string,
            api_id=self.session.api_id, api_hash=self.session.api_hash,
            proxy=repo.proxies.get_dict(proxy_id=sp.proxy_id)
        )

    def logger(self, txt):
        logger.info(f"[{self.prefix}] {txt}")

    async def start_session(self):
        await self.client.start()

    async def stop_session(self):
        await self.client.stop()

    async def all_connection(self):
        self.client = await self.open_session()
        if not self.client:
            raise
        self.executor = BotExecutorAction(client=self.client, session=self.session)
        self.tasker = BotTaskerAction(client=self.client, session=self.session, executor=self.executor)
        self.simulator = SimulatorAction(client=self.client)

    async def check(self, chat_id: [int, str] = "durov") -> bool:
        try:
            await self.start_session()
            await self.executor.get_chat(chat_id=chat_id)

            repo.sessions.update(self.session, state=SessionStates.free)
            await self.stop_session()
            return True
        except:
            await self.executor.session_banned()
            return False

    #
    # async def spam_bot_check(self):
    #     try:
    #         await asyncio.sleep(await smart_sleep(self.session))
    #         chat_id = "SpamBot"
    #         self.logger("Начинаю проверку")
    #         await self.start_session()
    #         await self.executor.send_message(chat_id, '/start')
    #         self.logger("Отправил start")
    #         while True:
    #             msg = (await self.executor.get_chat_history(chat_id, limit=1))[0]
    #             try:
    #                 keyboard = msg.reply_markup.keyboard
    #             except:
    #                 keyboard = None
    #             if keyboard:
    #                 if str(keyboard) in SPAM_REPLY_ANSWERS:
    #                     self.logger(f"Ответ: {SPAM_REPLY_ANSWERS[str(keyboard)]}")
    #                     await self.executor.send_message(chat_id=chat_id, text=SPAM_REPLY_ANSWERS[str(keyboard)])
    #                     await asyncio.sleep(5)
    #                 else:
    #                     self.logger(f"Найден новый ответ: \n{msg.text}\n{msg.reply_markup.keyboard}")
    #                     break
    #             elif msg.text in SPAM_STOP_MESSAGE:
    #                 self.logger("СТОП")
    #                 break
    #             elif msg.text in SPAM_MESSAGE_ANSWERS:
    #                 await self.executor.send_message(chat_id=chat_id, text=SPAM_MESSAGE_ANSWERS[msg.text])
    #                 await asyncio.sleep(5)
    #             else:
    #                 self.logger(f"Найден новый ответ: \n{msg.text}")
    #                 break
    #
    #             if msg.text in SPAM_FREE_MESSAGE:
    #                 self.logger("КАЕФ")
    #                 await self.client.stop()
    #                 return True
    #         await self.client.stop()
    #         return False
    #     except errors.UserDeactivatedBan:
    #         await self.executor.session_banned()
    #         return False
    #     except errors.AuthKeyDuplicated:
    #         await self.executor.session_banned()
    #         return

    """

        MAIN FUNCTION

    """

    @func_logger
    async def start(self):
        self.logger(f"Started!")
        await self.all_connection()
        while True:
            await asyncio.sleep(await smart_sleep(self.session))
            my_tasks = repo.sessions_tasks.get_all(
                in_list=True, session=self.session, state=SessionTaskStates.enable
            )
            if my_tasks:
                self.logger("Find task")
                try:
                    await self.start_session()
                    while my_tasks:
                        for task in my_tasks:
                            await self.start_answers()
                            await asyncio.sleep(await smart_sleep(self.session))
                            if task.type == SessionTaskType.join_group:  # JOIN GROUP
                                await self.tasker.join_group(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.check_group:  # CHECK GROUP
                                await self.tasker.check_group(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.send_by_order:  # SEND BY ORDER
                                await self.tasker.send_by_order(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.send_by_mailing:  # SEND BY MAILING
                                await self.tasker.send_by_mailing(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.change_fi:  # CHANGE FI
                                await self.tasker.change_fi(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.change_avatar:  # CHANGE AVATAR
                                await self.tasker.change_avatar(task)
                                await asyncio.sleep(await smart_create_sleep(self.session))
                            elif task.type == SessionTaskType.check_message:  # CHECK MESSAGE
                                await self.tasker.check_message(task)
                            else:
                                self.logger(f"Task not found {task.type}")
                            my_tasks = repo.sessions_tasks.get_all(
                                in_list=True, session=self.session, state=SessionTaskStates.enable
                            )
                        await asyncio.sleep(ASSISTANT_SLEEP_SEC)
                    await self.stop_session()
                except errors.UserDeactivatedBan:
                    self.logger("UserDeactivatedBan")
                    await self.executor.session_banned()
                    return
                except errors.AuthKeyDuplicated:
                    self.logger("AuthKeyDuplicated")
                    await self.executor.session_banned()
                    return
                except errors.InputUserDeactivated:
                    self.logger("InputUserDeactivated")
                    await self.stop_session()
            else:
                try:
                    self.logger("Not find task")
                    await self.start_session()
                    await self.start_answers()
                    await self.stop_session()
                except errors.UserDeactivatedBan:
                    self.logger("UserDeactivatedBan")
                    await self.executor.session_banned()
                    return
                except errors.AuthKeyDuplicated:
                    self.logger("AuthKeyDuplicated")
                    await self.executor.session_banned()
                    return
                except errors.InputUserDeactivated:
                    self.logger("InputUserDeactivated")
                    await self.stop_session()

            await asyncio.sleep(ASSISTANT_SLEEP_SEC)

    async def start_answers(self):
        try:
            async for dialog in self.client.get_dialogs(limit=100):
                if dialog.chat.type == enums.ChatType.PRIVATE:
                    if dialog.chat.id in self.black_list:
                        continue

                    async for msg in self.client.get_chat_history(chat_id=dialog.chat.id, limit=1):
                        if msg.from_user.id == self.session.tg_user_id:
                            continue

                        user: User = repo.users.create(tg_user_id=msg.from_user.id)
                        await self.executor.update_user(user=user, tg_user=msg.from_user)
                        repo.messages.create(
                            user=user, message_id=msg.id, text=msg.text or msg.caption, state=MessageStates.from_user
                        )

                        msg_send = await msg.reply("\n".join(ANSWER_MESSAGE), disable_web_page_preview=True)
                        if msg_send and not msg_send.empty:
                            if msg_send.from_user:
                                await self.executor.update_session(msg_send.from_user)

                        repo.messages.create(
                            user=user, message_id=msg_send.id, text=msg_send.text, state=MessageStates.to_user
                        )
                        await self.executor.send_message_answer_log(
                            session_id=self.session.id, username=msg.from_user.username, user_id=user.id
                        )
        except errors.UserDeactivatedBan:
            self.logger("UserDeactivatedBan")
            return await self.executor.session_banned()
        except errors.AuthKeyDuplicated:
            self.logger("AuthKeyDuplicated")
            return await self.executor.session_banned()
        except errors.ChannelPrivate:
            self.logger("ChannelPrivate")
        except errors.InputUserDeactivated:
            self.logger("InputUserDeactivated")
