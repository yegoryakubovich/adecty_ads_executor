import repo
from bot.sessions import session_actions
from models.sessions import SessionStates


async def check_banned(client):
    async with client:
        try:
            await client.get_chat('durov')
            return True
        except:
            return False


async def check_wait_sessions():
    for session in repo.sessions.get_all_by_state(state=SessionStates.wait):
        client = await session_actions.open_session(session)
        if await check_banned(client):
            repo.sessions.move_state(session, SessionStates.free)
        else:
            repo.sessions.move_state(session, SessionStates.banned)


async def check_free_sessions():
    for session in repo.sessions.get_all_by_state(state=SessionStates.free):
        client = await session_actions.open_session(session)
        if await check_banned(client):
            repo.sessions.move_state(session, SessionStates.free)
        else:
            repo.sessions.move_state(session, SessionStates.banned)
