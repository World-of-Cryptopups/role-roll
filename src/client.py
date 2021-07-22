from __future__ import annotations

from typing import Optional

import discord
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands import Context

from src.dps.command import DPS
from src.me.command import ME
from src.register.command import REGISTER
from src.roll.command import ROLL

# CREATE A NEW CLIENT
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=">", description="", intent=intents)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.command()
async def hello(ctx: Context):
    await ctx.send(
        "Hello! This bot is still under construction, please come back later"
    )


# >roll
@client.command()
async def roll(ctx: Context, name: Optional[str]):

    # check if name is blank or None
    if not name:
        await ctx.send("Please add your WAX ID to the command like: `>roll mywax.wam`")
        return

    # remove spaces
    _name = name.strip()

    # set fetching message
    msg: discord.Message = await ctx.send(f"Fetching DPS of **{_name}**...")

    # execute function and get message
    _message = ROLL(_name, ctx.author, False, None)

    # edit sent message and send it
    await msg.edit(content=f"<@!{ctx.author.id}>", embed=_message)


# >register
@client.command()
async def register(ctx: Context, token: Optional[str]):
    if not token:
        await ctx.send(
            "Please add your TOKEN ID to the command like: `>register given-token`. Please contact an admin if you are not sure what to do."
        )
        return

    m: discord.Message = await ctx.send(f"Registering <@!{ctx.author.id}>")

    # strip token
    _token = token.strip()

    _message = REGISTER(_token, ctx.author)

    await m.edit(content=_message)


# >dps
@client.command()
async def dps(ctx: Context):
    # get the author id
    _id = ctx.author.id

    # set fetching dps message
    msg: discord.Message = await ctx.send(f"Fetching DPS stats of **<@!{_id}>**...")

    # get the DPS
    _message: Embed | str = DPS(ctx.author)

    if type(_message) == str:
        await msg.edit(content=_message)
        return

    # edit sent message with the new content from DPS()
    await msg.edit(content=f"<@!{_id}>", embed=_message)


# >me
@client.command()
async def me(ctx: Context):
    _message = ME(ctx.author)

    await ctx.send(embed=_message)
