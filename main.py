import os
import discord
import logging


# load .envfile if in development
devel = os.getenv("DEVEL")
if devel:
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=".env.local")

client = discord.Client()
my_secret = os.getenv("TOKEN")


logger = logging.getLogger("discord")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
logger.addHandler(handler)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send(
            "Hello! This bot is still under construction, please come back later"
        )


client.run(my_secret)