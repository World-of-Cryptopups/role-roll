import asyncio
import itertools

import discord
import requests
from discord import activity
from discord.ext import tasks
from src.client import client
from src.lib.pups import SCHEMAS
from src.lib.tinydb import db
from tinydb.database import TinyDB

base_url = "https://wax.api.atomicassets.io/atomicassets/v1/assets?collection_name=cryptopuppie&schema_name={schema}&order=desc&sort=asset_id&limit=1000&page={page}"


@tasks.loop(minutes=5)
async def fetch_all_data():
    # wait for bot to be ready
    await client.wait_until_ready()

    while not client.is_closed():
        print("[FETCHER] Starting to fetch all datas again...")

        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, name="fetching..."
            )
        )

        with TinyDB("dps-download.json") as dlDB:
            # first drop the existing downloaded
            dlDB.drop_tables()

            with requests.Session() as session:
                for s in SCHEMAS:
                    # count start at 1
                    for i in itertools.count(1):
                        # handle JsonDecode errors
                        try:
                            d = session.get(base_url.format(schema=s, page=i))
                            r = d.json()
                        except Exception as e:
                            print(f"[error!] schema: {s}, page: {i}, error: {e}")
                            continue

                        if len(r["data"]) == 0:
                            break

                        dlDB.insert_multiple(r["data"])
                        print(f"[FETCHER] -> downloaded | schema: {s}, page: {i}")

                    print(f"[FETCHER] Done with {s}")

            # drop first the existing datas
            db.drop_tables()

            # insert datas to main db
            db.insert_multiple(dlDB.all())

        print("[FETCHER] Task done!")

        # change presense to wathing
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="World of Cryptopups"
            )
        )

        # run again after 5 minutes
        await asyncio.sleep(300)
