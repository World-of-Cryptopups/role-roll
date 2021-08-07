import asyncio
import itertools

import discord
import requests
from aiohttp import ClientSession
from discord import activity
from discord.ext import tasks
from src.client import client
from src.lib.pups import SCHEMAS
from src.lib.tinydb import db
from tinydb.database import TinyDB

base_url = "https://wax.api.atomicassets.io/atomicassets/v1/assets?collection_name=cryptopuppie&schema_name={schema}&order=desc&sort=asset_id&limit=1000&page={page}"


async def _fetcher(s: str, i: int, session: ClientSession, xdb: TinyDB):
    async with session.get(base_url.format(schema=s, page=i)) as resp:
        d = await resp.json()

        if len(d["data"]) == 0:
            return True

        xdb.insert_multiple(d["data"])
        print(f"[FETCHER] -> downloaded | schema: {s}, page: {i}")


async def _runner(s: str, i: int, session: ClientSession, xdb: TinyDB):
    try:
        return await _fetcher(s, i, session, xdb)
    except Exception as e:
        print(f"[error!] schema: {s}, page: {i}, error: {e}")
        # try again
        return await _runner(s, i, session, xdb)


async def _getter(s: str, xdb: TinyDB):
    async with ClientSession() as session:
        for i in itertools.count(1):
            x = await _runner(s, i, session, xdb)
            if x == True:
                break

        print(f"[FETCHER] Done with {s}")


async def _tasker():
    print("[FETCHER] Starting to fetch all datas again...")

    with TinyDB("dps-download.json") as xdb:
        x = await asyncio.gather(
            *[asyncio.ensure_future(_getter(s, xdb)) for s in SCHEMAS]
        )
        if x:
            # drop first the existing datas
            db.drop_tables()

            # insert datas to main db
            db.insert_multiple(xdb.all())

            print("[FETCHER] Task done!")


async def fetch_all_data():
    # wait for bot to be ready
    # await client.wait_until_ready()

    # while not client.is_closed():
    # print("[FETCHER] Starting to fetch all datas again...")

    # await client.change_presence(
    #     activity=discord.Activity(
    #         type=discord.ActivityType.listening, name="fetching..."
    #     )
    # )

    # with TinyDB("dps-download.json") as dlDB:
    #     # first drop the existing downloaded
    #     dlDB.drop_tables()

    #     with requests.Session() as session:
    #         for s in SCHEMAS:
    #             # count start at 1
    #             for i in itertools.count(1):
    #                 # handle JsonDecode errors
    #                 try:
    #                     d = session.get(base_url.format(schema=s, page=i))
    #                     r = d.json()
    #                 except Exception as e:
    #                     print(f"[error!] schema: {s}, page: {i}, error: {e}")
    #                     continue

    #                 if len(r["data"]) == 0:
    #                     break

    #                 dlDB.insert_multiple(r["data"])
    #                 print(f"[FETCHER] -> downloaded | schema: {s}, page: {i}")

    #             print(f"[FETCHER] Done with {s}")

    #     # drop first the existing datas
    #     db.drop_tables()

    #     # insert datas to main db
    #     db.insert_multiple(dlDB.all())

    while True:
        await _tasker()

        # print("[FETCHER] Task done!")

        # change presense to wathing
        # await client.change_presence(
        #     activity=discord.Activity(
        #         type=discord.ActivityType.watching, name="World of Cryptopups"
        #     )
        # )

        # run again after 5 minutes
        await asyncio.sleep(300)
