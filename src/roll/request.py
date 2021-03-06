import time
from typing import List

from requests import Session
from src.lib.pups import SCHEMAS
from src.lib.tinydb import db
from tinydb.queries import where

PUPSKINS_API = "https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=cryptopuppie&schema_name=pupskincards&page=1&limit=1000&order=desc&sort=asset_id"
PUPPYCARDS_API = "https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=cryptopuppie&schema_name=puppycards&page=1&limit=1000&order=desc&sort=asset_id"
PUPITEMS_API = "https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=cryptopuppie&schema_name=pupitems&page=1&limit=1000&order=desc&sort=asset_id"


_urls = [PUPSKINS_API, PUPPYCARDS_API, PUPITEMS_API]


def _fetch_request(url: str, session: Session):
    d = session.get(url).json()

    return {"url": url, "response": d}

    # async with session.get(url) as resp:
    #     d = await resp.json()

    #     return {"url": url, "response": d}


# requester for dps calculation
def requester(owner: str, urls: List[str]):
    with Session() as session:
        return [_fetch_request(i.format(owner=owner), session) for i in urls]


# calculates the dps from the `TinyDB` db
def calculator(owner: str):
    return [
        {
            "schema": i,
            "values": db.search(
                (where("owner") == owner) & (where("schema")["schema_name"] == i)
            ),
        }
        for i in SCHEMAS
    ]
