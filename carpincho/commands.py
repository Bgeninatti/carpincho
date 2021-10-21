import click

from carpincho.attendees.api.attendees import AttendeeProvider
from carpincho.attendees.api.client import EventolClient
from carpincho.bot.main import bot
from carpincho.db.models import init_db, Attendee
from carpincho.db.queries import get_next_attendee_id


@click.command()
@click.pass_context
def update_attendees(ctx):
    db_path = ctx.obj["DEFAULT"]["db_path"]
    fetch_limit = int(ctx.obj["DEFAULT"]["fetch_limit"])
    username = ctx.obj["EVENTOL"]["username"]
    passwrod = ctx.obj["EVENTOL"]["password"]

    init_db(db_path)
    latest_id = get_next_attendee_id()
    client = EventolClient(username, passwrod)
    fetcher = AttendeeProvider(client)
    print(f"Fetching attendees since: latest_id={latest_id} limit={fetch_limit}")
    new_attendees = list(fetcher.fetch_since(latest_id, fetch_limit))
    print(f"Saving new attendees: attendees_count={len(new_attendees)}")
    Attendee.bulk_create(new_attendees)


@click.command()
@click.pass_context
def run_bot(ctx):
    db_path = ctx.obj["DEFAULT"]["db_path"]
    token = ctx.obj["DISCORD"]["token"]

    init_db(db_path)
    bot.run(token)
