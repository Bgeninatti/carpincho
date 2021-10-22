import asyncio
from datetime import datetime
from typing import Tuple, Optional

import discord
from discord.ext import commands

from carpincho.config import load_config
from carpincho.db.models import RegistrationStatus, Attendee
from carpincho.db.queries import find_attendee, get_status
from carpincho.logger import get_logger

log = get_logger(__name__)
config = load_config()

CHANNEL = config["DISCORD"]["channel"]
ADMIN_CHANNEL = config["DISCORD"]["admin_channel"]
ROLE = config["DISCORD"]["role"]

bot = commands.Bot(command_prefix="\\")


def register_attendee(word: str, msg) -> Tuple[RegistrationStatus, Optional[Attendee]]:

    attendee = find_attendee(word)
    if not attendee:
        return RegistrationStatus.NOT_FOUND, None

    elif attendee.status == RegistrationStatus.OK.name:
        return RegistrationStatus.ALREADY_REGISTERED, attendee

    elif attendee.status == RegistrationStatus.PENDING.name:
        attendee.status = RegistrationStatus.OK.name
        attendee.discord_user = msg.author
        attendee.updated = datetime.now()
        attendee.save()
        log.info(
            "Registering attendee",
            extra={'attendee_id': attendee.attendee_id, 'discord_user': attendee.discord_user}
        )
        return RegistrationStatus.OK, attendee
    else:
        raise ValueError("IDK what happened. But looks bad.")


@bot.command(name="ping", help="Comando de prueba", pass_context=True)
async def ping(ctx):
    if str(ctx.channel) == ADMIN_CHANNEL:
        await ctx.send("pong")


@bot.command(name="estado", help="Comando para ver el estado actual de regitros", pass_context=True)
async def estado(ctx):
    if str(ctx.channel) != ADMIN_CHANNEL:
        # Remove messages when not on the specific attendees channel
        await discord.Message.delete(ctx.message)
    else:
        status = get_status()
        total = sum(v for v in status.values())
        msg = '\n'.join(f"{key.lower()}: {value}" for key, value in status.items())
        msg += f'\n\nTOTAL: {total}'
        await ctx.send(msg)


@bot.command(name="registro", help="Comando de registro", pass_context=True)
async def registro(ctx, word: str):

    if str(ctx.channel) != CHANNEL:
        # Remove messages when not on the specific attendees channel
        await discord.Message.delete(ctx.message)
        return

    role_exists = [r for r in ctx.message.author.roles if r.name.lower() == ROLE]
    if role_exists:
        msg = f"{ctx.message.author.mention} ya estás registrado!"
        message = await ctx.send(msg)
        await asyncio.sleep(5)
        await discord.Message.delete(message)
        return
    status, attendee = register_attendee(word, ctx.message)

    if status == RegistrationStatus.NOT_FOUND:
        msg = ("No encontré un registro con esos datos :(\n "
               "Si te registraste recién probá de nuevo en 10 minutos.")
        message = await ctx.send(msg)
        await asyncio.sleep(5)
        await discord.Message.delete(message)
    elif status == RegistrationStatus.ALREADY_REGISTERED:
        msg = "Ticket ya registrado"
        message = await ctx.send(msg)
        await asyncio.sleep(5)
        await discord.Message.delete(message)
    else:
        # Load special role to give permissions
        role = discord.utils.get(ctx.message.author.guild.roles, name=ROLE)
        msg = f"Usuario {ctx.message.author.mention} registrado! :)"
        await ctx.author.add_roles(role)
        # Send final response
        await ctx.send(msg)

    # Remove command after parsing it
    await discord.Message.delete(ctx.message)

# Removing help command
bot.remove_command("help")
