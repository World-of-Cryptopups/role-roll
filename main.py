import os

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


# run bot
client.run(my_secret)
