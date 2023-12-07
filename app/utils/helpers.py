from datetime import datetime, timedelta
from random import randint

from loguru import logger

from database import repo
from database.models import SleepStates, Session


async def smart_create_sleep(session: Session, minimum: int, maximum: int):
    logger.info("smart_create_sleep")
    for sleep in repo.sleeps.get_all(session=session, state=SleepStates.enable):
        logger.info(f"Sleep #{sleep.id} (session_{session.id}) disabled by smart_create_sleep")
        repo.sleeps.update(sleep, state=SleepStates.disable)
    repo.sleeps.create(session=session, time_second=randint(minimum, maximum), state=SleepStates.enable)
    return await smart_sleep(session)


async def smart_sleep(session: Session):
    logger.info("smart_sleep")
    sleeps = repo.sleeps.get_all(session=session, state=SleepStates.enable)
    if not sleeps:
        logger.info(f"No found sleep (session_{session.id})")
        return 0
    for sleep in sleeps:
        delta = (sleep.created + timedelta(seconds=sleep.time_second)) - datetime.utcnow()
        delta_sec = int(delta.total_seconds())
        if delta_sec <= 0:
            logger.info(f"Sleep #{sleep.id} (session_{session.id}) disabled by smart_sleep")
            repo.sleeps.update(sleep, state=SleepStates.disable)
            return 0
        logger.info(f"[SLEEP #{sleep.id}] Session #{session.id} {delta}")
        return delta_sec
