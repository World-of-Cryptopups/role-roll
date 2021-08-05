import os

from tasks.fetcher import fetch_all_data

# load .envfile if in development
devel = os.getenv("DEVEL")
if devel:
    from dotenv import load_dotenv

    load_dotenv()

from logger import setup_logger
from src.client import client

# get TOKEN from environment
my_secret = os.getenv("TOKEN")


# setup logger
setup_logger()


fetch_all_data.start()

# run bot
client.run(my_secret)
