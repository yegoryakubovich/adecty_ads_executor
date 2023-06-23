from database import repo
from database.models import Order, SessionStates, GroupStates


async def smart_send_message(order: Order):
    for free_session in repo.sessions.get_all_by_state(state=SessionStates.free):
        for group in repo.groups.get_all_by_state(state=GroupStates.active):
            pass
