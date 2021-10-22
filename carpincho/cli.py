import click

from carpincho.commands import update_attendees, run_bot, run_monitor
from carpincho.config import load_config


@click.group(name='carpincho')
@click.pass_context
def main(ctx):
    """Carpincho CLI"""
    ctx.ensure_object(dict)
    ctx.obj.update(load_config())


main.add_command(update_attendees)
main.add_command(run_bot)
main.add_command(run_monitor)
