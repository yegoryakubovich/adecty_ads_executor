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
            text = text.replace(latter, choice(LATTERS[latter]))
        return text

    """LOGGING"""

    async def send_log_message(self, text):
        bot = Bot(token=self.token)
        # return await bot.send_message(chat_id=self.chat_id, text=text)
        return logger.info(text)

    @staticmethod
    async def create_link(group_name, post_id):
        return f"<a href='https://t.me/{group_name}/{post_id}'>@{group_name}</a>"

    async def proxy_disable_log(self, proxy_id: int,
                                proxy_shop_id: int, proxy_shop_name: str):
        return await self.send_log_message(text="\n".join([
            f"🚫 Прокси #{proxy_id} заблокирован",
            f"Магазин: {proxy_shop_name}({proxy_shop_id})",
            "",
            f"#proxy_{proxy_id} #proxy_shop_{proxy_shop_id}"
        ]))

    async def session_banned_log(self, session_id: int, proxy_id: int,
                                 session_shop_id: int, session_shop_name: str,
                                 proxy_shop_id: int, proxy_shop_name: str,
                                 messages_send: int):
        return await self.send_log_message(text="\n".join([
            f"🚫 Сессия #{session_id} заблокирована",
            f"Сессия из {session_shop_name}, прокси из {proxy_shop_name}",
            f"Всего сообщений: {messages_send}",
            "",
            f"#session_{session_id} #proxy_{proxy_id} #session_shop_{session_shop_id} #proxy_shop_{proxy_shop_id}"
        ]))

    async def session_added_log(self, session_id: int, session_shop_id: int, session_shop_name: str):
        return await self.send_log_message(text="\n".join([
            f"➡️ Сессия #{session_id} успешно добавлена."
            f"Магазин: {session_shop_name}",
            f"",
            f"#session_{session_id} #session_shop_{session_shop_id}",
        ]))

    async def proxy_added_log(self, proxy_id: int, proxy_shop_id: int, proxy_shop_name: str, ):
        return await self.send_log_message(text="\n".join([
            f"➡️ Прокси: #{proxy_id}) успешно добавлена.",
            f"Магазин: #{proxy_shop_name}) успешно добавлена.",
            f"",
            f"#proxy_{proxy_id} #proxy_shop_{proxy_shop_id}",
        ]))

    async def send_message_log(self, session_id: int,
                               order_id: int, order_name: str,
                               group_id: int, group_name: str, post_id: int,
                               session_messages_count: int):
        link = self.create_link(group_name=group_name, post_id=post_id)
        return await self.send_log_message(text="\n".join([
            f"️✉️ Сессия(id: {session_id}) направила ообщение по объявлению {order_name}(#{order_id}) в {link}.",
            f"Всего сообщений: {session_messages_count}.",
            f"",
            f"# session_{session_id}",
            f"# group_{group_id}",
        ]))
