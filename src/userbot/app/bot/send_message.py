import repo
from models import Order
from models.groups import GroupStates
from models.sessions import SessionStates


async def smart_send_message(order: Order):
    for free_session in repo.sessions.get_all_by_state(state=SessionStates.free):
        for group in repo.groups.get_all_by_state(state=GroupStates.active):
            pass
