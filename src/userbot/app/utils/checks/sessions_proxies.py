from database import repo
from database.models import Session


async def find_new_link(session: Session):
    return repo.sessions_proxies.create(session=session, proxy=repo.sessions_proxies.get_free_proxy())[0]

# async def check_link_sessions():
#     for session in repo.sessions.get_all_enable():
#         client = await session_actions.open_session(session)
#         async with client:
#             try:
#                 await client.get_entity('durov')
#                 if session.id == 1:
#                     raise UserDeactivatedBanError
#             except (UserDeactivatedBanError, UnauthorizedError):
#                 repo.sessions.move_state(SessionStates.banned)
