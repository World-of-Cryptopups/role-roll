from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import Context

from src.dps.command import DPS
from src.me.command import ME
from src.register.command import REGISTER
from src.roll.commands import ROLL

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
    if not name:
        await ctx.send("Please add your WAX ID to the command like: `>roll mywax.wam`")
        return

    msg: discord.Message = await ctx.send(f"Fetching DPS of **{name}**...")

    # remove spaces
    _name = name.strip()
    _message = await ROLL(_name, ctx.author)

    await msg.edit(content=f"<@!{ctx.author.id}>", embed=_message)


# >register
@client.command()
async def register(ctx: Context, token: Optional[str]):
    if not token:
        await ctx.send(
            "Please add your TOKEN ID to the command like: `>register given-token`. Please contact an admin if you are not sure what to do."
        )
        return

    # strip token
    _token = token.strip()

    _message = await REGISTER(_token, ctx.author)

    await ctx.send(_message)


# >dps
@client.command()
async def dps(ctx: Context):
    _message = await DPS(ctx.author)

    msg: discord.Message = await ctx.send(
        f"Fetching DPS stats of **<@!{ctx.author.id}>**..."
    )
    await msg.edit(content=f"<@!{ctx.author.id}>", embed=_message)


# >me
@client.command()
async def me(ctx: Context):
    _message = await ME(ctx.author)

    await ctx.send(embed=_message)
