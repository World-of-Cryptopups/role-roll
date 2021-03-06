import asyncio
import os
import time

# load .envfile if in development
devel = os.getenv("DEVEL")
if devel:
    from dotenv import load_dotenv

    load_dotenv()

from logger import setup_logger
from src.client import client
from tasks.fetcher import fetch_all_data

# get TOKEN from environment
my_secret = os.getenv("TOKEN")


# setup logger
setup_logger()

# client.loop.create_task(fetch_all_data())
time.sleep(10)


# run bot
client.run(my_secret)
