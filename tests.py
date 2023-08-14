import asyncio

from pyrogram import Client

a = "BQAAB_gAwY-GjVGJDGZpUS1JIwd-g5hql7BfT1RLOWjAFUJRwyYlyilrmQ0YLHXFtWAm7noVoQ6nvk7Zp9gnhYnp9GdvsMtcPfNWwwo1znUx2cqcRPkyn8OZlUdmm3qEdzIhetdZ3_6r1TL74I3yoa3DIfsuNASfPW0RCldQ9upOeE-YA7Wha5IdTBmO-p7JjHG5g39HKvduZJEVphXgawHfLVJerQUovOF1hTjGiiN-Dqlktv46SqSeJL_yKOCeA0TUI6P5BlqMYVOzkO0j-buOGPWrhZvufc9UUQmjBzCqIMQV2kBzZ0PZU7PRMrMCkAzUdqB735aw5MsbFmcKxcHM-0JSVgAAAAF8Q4mAAA"


async def main():
    client = Client("LOL", session_string=a)
    async with client:
        await client.send_message(chat_id=451867324, text="Hello")
        r = await client.get_users(user_ids="451867324")
        print(r)


asyncio.run(main())
