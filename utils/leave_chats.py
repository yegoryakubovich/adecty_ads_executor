import asyncio

from loguru import logger
from pyrogram import Client, errors
from pyrogram.enums import ChatType

session_string = "BAAAB_gAUW_wNumj-nz470Y10-kfhX4mTh3cQof6Embib4qxxzpAn5j-BcoJ80Xz7Z-MQk6VKS1G6AdGvVz_GjJ_SB7YOdI5ySzqpvDzviguZXN3pQ7VNgMO43499Mf3Z8SwbzldUaTdIroOA0kDJN05B3eXl3fTXevUL_65llSsXNoS3DJvn-MAnd8WF3s74M-OV8sj9bYaabfueeR1_tUkD1xY-vNxAoZnf-OVW1pLxnfCtij_uOrTsWHOuE83ROBcWszxV4RMHzRIS9EE-ZDgJlJC_WFxfznMy7N_-WPTkEDKxMSOOkyNbLQj7XllZuP3W2c2VPu6hxpoTyDbH4tRzT_WsAAAAAGYM5M7AA"


async def main():
    i = 0
    client = Client(name="lol", session_string=session_string)
    await client.start()
    async for dialog in client.get_dialogs():
        if i > 100:
            break
        logger.info(f"{dialog.chat.id} {dialog.chat.username}")
        if dialog.chat.type in [ChatType.BOT, ChatType.PRIVATE]:
            continue
        await asyncio.sleep(0.05)
        try:
            i += 1
            await client.leave_chat(chat_id=dialog.chat.id)
            await asyncio.sleep(0.1)
        except errors.ChannelPrivate:
            pass
    await client.stop()


asyncio.run(main())
