import asyncio

from pyrogram import Client
from pyrogram.filters import private
from pyrogram.types import Message

a = "BAAAB_gAIzEMws-y1mAEUgog1qevfg0daR_lGMVblNh6bVnCKfomvk4LXrmxCqNLiKUPAdpZGN_bIFqZny4gHkexcDe1jy-bboru8M4JwQBHDo3dyIlG-0R1OttXUCn4B3WVY_hyO4uuttD2WztoYDWUcBsd77-GJaDG5jpWVQI1VDVZy3AyGvFRLYyP5pD8OuDgwQX9t3rSzs4iN0faZNnAcPb5_FxNumMF4KjdQb2FbZvpYkCziWO5tVrOEKuGGgC0yN3fAANtdFcnwr0V-F4KuZ7Wc7zo_-LPZY-l1P7FhMdQRtAUxsthuR3nf0ZFoHbKOEK8DbkqVOzMIE3NPRkXgIwUJwAAAAGYKLIqAA"
telegram_id = 6847771178
client = Client("LOL", session_string=a)


async def main():
    client = Client("LOL", session_string=a)

    #
    # async for dialog in client.get_dialogs(limit=100):
    #     if dialog.chat.type != enums.ChatType.PRIVATE:
    #         continue
    #     if dialog.chat.id in [telegram_id, 777000]:
    #         logger.info(f"id {dialog.chat.id}")
    #         continue
    #
    #     async for msg in client.get_chat_history(chat_id=dialog.chat.id, limit=1):
    #         if msg.from_user.id == telegram_id:
    #             logger.info(f"msg id {msg.from_user.id}")
    #             continue
    #         if msg.empty:
    #             logger.info(f"empty {msg.empty}")
    #             continue
    #
    #         logger.info(f"Ответ на {msg.text or msg.caption}")
    # await client.stop()


asyncio.run(main())
