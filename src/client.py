from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands import Context

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


@client.command()
async def roll(ctx: Context, name: Optional[str]):
    if not name:
        await ctx.send("Please add your WAX ID to the command like: `>roll mywax.wam`")
        return

    # remove spaces
    _name = name.strip()

    _message = await ROLL(_name, ctx.author)

    await ctx.send(f"<@!{ctx.author.id}>", embed=_message)