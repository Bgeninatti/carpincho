import click

from carpincho.attendees.api.attendees import AttendeeProvider
from carpincho.attendees.api.client import EventolClient
from carpincho.bot.main import bot
from carpincho.db.models import init_db, Attendee
from carpincho.db.queries import get_next_attendee_id
from carpincho.logger import get_logger

log = get_logger(__name__)


@click.command()
@click.pass_context
def update_attendees(ctx):
    fetch_limit = int(ctx.obj["EVENTOL"]["fetch_limit"])
    username = ctx.obj["EVENTOL"]["username"]
    passwrod = ctx.obj["EVENTOL"]["password"]
    init_db()
    latest_id = get_next_attendee_id()
    client = EventolClient(username, passwrod)
    fetcher = AttendeeProvider(client)

    log.info("Fetching attendees since: latest_id=%d limit=%d", latest_id, fetch_limit)
    new_attendees = list(fetcher.fetch_since(latest_id, fetch_limit))
    log.info("Saving new attendees: attendees_count=%d", len(new_attendees))
    Attendee.bulk_create(new_attendees)


@click.command()
@click.pass_context
def run_bot(ctx):
    token = ctx.obj["DISCORD"]["token"]
    log.info("Starting Discrod bot")

    init_db()
    bot.run(token)
