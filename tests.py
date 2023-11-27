import asyncio

from pyrogram import Client

a = "BAAAB_gAHiL7VGqngh_4XZvQfWerPU7cGrL8drN49_XJ41AP_gHgtEwqMg84-F96A04i_D68baRjqO2_tEzlQWrQsTP0Het2Usm-EMRHl-X6xfTBJh3JgT5ipQXDDCiCjNSJc9Tx6bTEoqNT6p4MSX8oZS9v3wZMEqgfkul9O6Ykh9p2VtoaOiIQM2XVn5wN5FSIj6YP7Q69GxAsvoEQZHmuVhAQ9IKoJ0dNIVoUMc9hsC8XE-qHYbipyIzp34viGGw1_j9A1LvBicGhffy-woBeCbIBOdHi0f61Z0dan6KBLQkr-cQ7sqmPRM7iAlOdHR_2qeUGV0tjVzClTF7zO0kZzpM1MwAAAAGGWASbAA"


async def main():
    client = Client("LOL", session_string=a)
    await client.start()
    result = [message.id async for message in client.get_chat_history(chat_id="ca_miami_chat", limit=30)]
    print(result)
    print(45010 in result)
    await client.stop()


asyncio.run(main())
