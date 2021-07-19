import os

from logger import setup_logger
from src.client import client

# load .envfile if in development
devel = os.getenv("DEVEL")
if devel:
    from dotenv import load_dotenv

    load_dotenv(dotenv_path=".env.local")


# get TOKEN from environment
my_secret = os.getenv("TOKEN")


# setup logger
setup_logger()


# run bot
client.run(my_secret)
