import re
from typing import Dict

from peewee import fn

from carpincho.db.models import Attendee

EMAIL_PATTERN = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', re.IGNORECASE)


def is_email(word):
    return EMAIL_PATTERN.fullmatch(word) is not None


def get_next_attendee_id() -> int:
    latest = Attendee.select().order_by(Attendee.attendee_id.desc()).first()
    if latest:
        return latest.attendee_id + 1
    else:
        return 5848  # First registered attendee for PyConAr2021


def get_status() -> Dict[str, int]:
    query = Attendee.select(
        Attendee.status,
        fn.Count(Attendee.status).alias('count')
    ).group_by(Attendee.status)

    return {r.status: r.count for r in query}


def find_attendee(word: str):
    # word can be an email or ticket code
    if is_email(word):
        return Attendee.select().where(Attendee.email == word.lower()).first()
    elif len(word) == 21:
        return Attendee.select().where(Attendee.ticket == word.lower()).first()
    else:
        return
