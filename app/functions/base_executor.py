from datetime import datetime, timedelta
from random import choice

from aiogram import Bot
from loguru import logger

from core.config import settings
from core.constants import LATTERS


class BaseExecutorAction:

    def __init__(self):
        self.token = settings.TELEGRAM_TOKEN
        self.chat_id = settings.TELEGRAM_CHAT_ID

    """COMMON"""

    async def replace_text(self, text: str):
        for latter in LATTERS:
            if LATTERS[latter]:
                text = text.replace(latter.lower(), choice(LATTERS[latter]))
                text = text.replace(latter.upper(), choice(LATTERS[latter]))
        return text

    @staticmethod
    async def create_link(group_name, post_id):
        return f"<a href='https://t.me/{group_name}/{post_id}'>@{group_name}</a>"

    @staticmethod
    async def create_user_link(username, user_id):
        return f"<a href='tg://user?id={user_id}'>@{username}</a>"

    """LOGGING"""

    # SEND MESSAGE
    async def send_log_message(self, text):
        bot = Bot(token=self.token, parse_mode="HTML")
        return await bot.send_message(chat_id=self.chat_id, text=text, disable_web_page_preview=True)
        return logger.info(text)

    async def proxy_disable_log(self, proxy_id: int,
                                proxy_shop_id: int, proxy_shop_name: str):
        return await self.send_log_message(text="\n".join([
            f"🚫 Прокси #{proxy_id} заблокирован",
            f"Магазин: {proxy_shop_name}({proxy_shop_id})",
            "",
            f"#disable_proxy #proxy_{proxy_id} #proxy_shop_{proxy_shop_id}"
        ]))

    async def session_banned_log(self, messages_send: int,
                                 session_id: int, session_shop_id: int, session_shop_name: str,
                                 proxy_id: int, proxy_shop_id: int, proxy_shop_name: str):
        return await self.send_log_message(text="\n".join([
            f"🚫 Сессия #{session_id} заблокирована",
            f"Сессия из {session_shop_name}, прокси из {proxy_shop_name}",
            f"Всего сообщений: {messages_send}",
            "",
            f"#ban_session #session_{session_id} #proxy_{proxy_id} #session_shop_{session_shop_id} #proxy_shop_{proxy_shop_id}"
        ]))

    async def new_session_banned_log(self, session_id: int,
                                     session_shop_id: int, session_shop_name: str):
        return await self.send_log_message(text="\n".join([
            f"🚫 Сессия #{session_id} не прошла проверку",
            f"Сессия из {session_shop_name}",
            "",
            f"#ban_new_session #session_{session_id} #session_shop_{session_shop_id}"
        ]))

    async def session_added_log(self, session_id: int, session_shop_id: int, session_shop_name: str):
        return await self.send_log_message(text="\n".join([
            f"➡️ Сессия #{session_id} успешно добавлена",
            f"Магазин: {session_shop_name}",
            f"",
            f"#new_session #session_{session_id} #session_shop_{session_shop_id}",
        ]))

    async def proxy_added_log(self, proxy_id: int, proxy_shop_id: int, proxy_shop_name: str, ):
        return await self.send_log_message(text="\n".join([
            f"➡️ Прокси: #{proxy_id} успешно добавлена",
            f"Магазин: {proxy_shop_name}",
            f"",
            f"#new_proxy #proxy_{proxy_id} #proxy_shop_{proxy_shop_id}",
        ]))

    async def send_message_log(self, session_id: int,
                               order_id: int, order_name: str,
                               group_id: int, group_name: str, post_id: int,
                               session_messages_count: int):
        link = await self.create_link(group_name=group_name, post_id=post_id)
        return await self.send_log_message(text="\n".join([
            f"️✉️ Сессия #{session_id} направила рекламу",
            f"Заказ: #{order_id} - {order_name}",
            f"Сообщение: {link}",
            f"Всего сообщений: {session_messages_count}",
            f"",
            f"#send_ads #session_{session_id} #group_{group_id} #order_{order_id}",
        ]))

    async def send_message_answer_log(self, session_id: int, username: str, user_id: int):
        user_link = await self.create_user_link(username=username, user_id=user_id)
        return await self.send_log_message(text="\n".join([
            f"️✉️ Сессия #{session_id} направила ответ",
            f"клиент: <b>{user_link}</b>",
            f"",
            f"#send_answer #session_{session_id} #user_{user_id}"
        ]))

    async def send_message_mailing_log(self,
                                       session_id: int, username: str, user_id: int, order_id: int, order_name: str):
        user_link = await self.create_user_link(username=username, user_id=user_id)
        return await self.send_log_message(text="\n".join([
            f"️✉️ Сессия #{session_id} направила сообщение рассылки",
            f"Заказ: <b>#{order_id} - {order_name}</b>"
            f"Клиент: <b>{user_link}</b>"
            f"",
            f"#send_mailing #session_{session_id} #user_{user_id} #order_{order_id}"
        ]))

    # Change message

    async def change_log_message(self,
                                 order_name: str, chat_id: int, message_id: int,
                                 text: str, presence_count: int, all_count: int, msg_count: int,
                                 sessions_free: int, sessions_spam: int):
        bot = Bot(token=self.token, parse_mode="HTML")
        data = (datetime.utcnow() + timedelta(hours=3)).strftime("%d.%m.%y %H:%M")
        return await bot.edit_message_text(
            chat_id=chat_id, message_id=message_id, disable_web_page_preview=True,
            text=f"\n".join([
                f"Заказ: <b>{order_name}</b> ({presence_count}/{all_count})",
                f"Сообщений за 24ч: {msg_count}",
                f"Сессий актив/спам: {sessions_free}/{sessions_spam}",
                f"Изменено: {data}",
                f"",
                text
            ])
        )
