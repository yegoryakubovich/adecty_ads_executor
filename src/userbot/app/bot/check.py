import asyncio

from telethon import TelegramClient

import repo


async def check_account(session_id: int) -> bool:
    session_dict = repo.sessions.get_dict(session_id)
    proxy = repo.proxies.get_random_dict()

    app = TelegramClient(**session_dict, proxy=proxy)
    async with app:
        r = await app.get_me()
    print(r)

    return True


async def check_all():
    tasks = []
    for session in repo.sessions.get_all():
        tasks.append(
            asyncio.create_task(
                check_account(session.id)
            )
        )
    for task in tasks:
        await task
