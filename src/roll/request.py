from aiohttp import ClientSession

PUPSKINS_API = "https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=cryptopuppie&schema_name=pupskincards&page=1&limit=1000&order=desc&sort=asset_id"
PUPPYCARDS_API = "https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=cryptopuppie&schema_name=puppycards&page=1&limit=1000&order=desc&sort=asset_id"
PUPITEMS_API = "https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=cryptopuppie&schema_name=pupitems&page=1&limit=1000&order=desc&sort=asset_id"


_urls = [PUPSKINS_API, PUPPYCARDS_API, PUPITEMS_API]


async def _fetch_request(url: str, session: ClientSession):
    async with session.get(url) as resp:
        d = await resp.json()

        return {"url": url, "response": d}


# requester for dps calculation
async def requester(owner: str):
    async with ClientSession() as session:
        return [await _fetch_request(i.format(owner=owner), session) for i in _urls]
