from pyrogram import Client


class ExecutorAction:
    def __init__(self, client: Client):
        self.client = client
        pass

    async def send_message(self, chat_id: int, text: str):
        await self.client.send_message(chat_id, text)

    async def join_chat(self, chat_id: int):
        await self.client.join_chat(chat_id)
