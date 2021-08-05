import itertools
import logging
from typing import Iterable, List, Mapping

import requests
from discord.ext import tasks
from src.lib import pups
from src.lib.pups import SCHEMAS
from src.lib.tinydb import db

base_url = "https://wax.api.atomicassets.io/atomicassets/v1/assets?collection_name=cryptopuppie&schema_name={schema}&order=desc&sort=asset_id&limit=1000&page={page}"


@tasks.loop(minutes=5)
async def fetch_all_data():
    pups.FETCHING = True

    # first drop the existing datas
    db.drop_table("assets")

    # new table
    assets = db.table("assets")

    print("[FETCHER] Starting to fetch all datas again...")

    with requests.Session() as session:
        for s in SCHEMAS:
            # count start at 1
            for i in itertools.count(1):
                r = session.get(base_url.format(schema=s, page=i)).json()

                if len(r["data"]) == 0:
                    break
                
                print(len(r['data']))

                assets.insert_multiple(r['data'])


            print(f"[FETCHER] Done with {s}")


    pups.FETCHING = False

    print("[FETCHER] Task done!")
