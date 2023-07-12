from datetime import datetime, timedelta
from random import randint

from loguru import logger

from core.constants import BOT_SLEEP_MIN_SEC, BOT_SLEEP_MAX_SEC
from database import repo
from database.models import SleepStates, Session


async def smart_create_sleep(session: Session, mi=BOT_SLEEP_MIN_SEC, ma=BOT_SLEEP_MAX_SEC):
    for sleep in repo.sleeps.get_all(session=session, state=SleepStates.enable):
        repo.sleeps.update(sleep, state=SleepStates.disable)
    repo.sleeps.create(session=session, time_second=randint(mi, ma))
    return await smart_sleep(session)


async def smart_sleep(session: Session):
    sleeps = repo.sleeps.get_all(session=session, state=SleepStates.enable)
    if not sleeps:
        return 0
    for sleep in sleeps:
        delta = (sleep.created + timedelta(seconds=sleep.time_second)) - datetime.utcnow()
        delta_sec = int(delta.total_seconds())
        if delta_sec <= 0:
            repo.sleeps.update(sleep, state=SleepStates.disable)
            return 0
        logger.info(f"[SLEEP #{sleep.id}] Session #{session.id} {delta}")
        return delta_sec

