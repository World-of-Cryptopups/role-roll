import os
import discord
from discord.ext import commands
from discord.ext.commands import Context
from logger import setup_logger


# load .envfile if in development
devel = os.getenv("DEVEL")
if devel:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=".env.local")


# get TOKEN from environment
my_secret = os.getenv("TOKEN")

# CREATE A NEW CLIENT
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=">", description="", intent=intents)

# logger
setup_logger()


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.command()
async def hello(ctx: Context):
    await ctx.channel.send(
        "Hello! This bot is still under construction, please come back later"
    )


# run bot
client.run(my_secret)
