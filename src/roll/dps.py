from typing import List

from src.roll.request import requester


# calculates the dps from data
def calculateDPS(owner: str, data: List) -> int:
    return sum(int(i["data"]["DPS"]) for i in data if owner == i["owner"])


_demon = ["Demon Queen", "Demon Ace", "Demon King"]
_mecha = ["Mecha Glitter", "Mecha Apollo", "Mecha Draco"]


# calculates the real dps
def calculateItemsDPS(basis: List, data: List, owner: str) -> int:
    dps = 0

    for i in data:
        for k in basis:
            _name = k["data"]["name"].strip()

            if _name in _demon:
                _name = "Demon"
            elif _name in _mecha:
                _name = "Mecha"

            if _name == i["data"]["Item Owner"].strip() and owner == i["owner"]:
                dps += int(i["data"]["DPS"])
                break

    return dps


PUPCARDS_TRUE = "https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=cryptopuppie&schema_name=puppycards&before=1626627600000&page=1&limit=1000&order=desc&sort=asset_id"
PUPSKINS_TRUE = "https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=cryptopuppie&schema_name=pupskincards&before=1626627600000&page=1&limit=1000&order=desc&sort=asset_id"
PUPITEMS_TRUE = "https://wax.api.atomicassets.io/atomicassets/v1/assets?owner={owner}&collection_name=cryptopuppie&schema_name=pupitems&before=1626627600000&page=1&limit=1000&order=desc&sort=asset_id"


# a special function for getting the owner's true DPS from events
def getSeasonPassDPS(owner: str) -> int:
    resps = requester(owner, [PUPCARDS_TRUE, PUPSKINS_TRUE, PUPITEMS_TRUE])

    # calculate all dps
    puppyCardsDPS = calculateDPS(owner, resps[0]["response"]["data"])
    pupSkinsDPS = calculateDPS(owner, resps[1]["response"]["data"])
    pupItemsRealDPS = calculateItemsDPS(
        resps[1]["response"]["data"], resps[2]["response"]["data"], owner
    )

    return puppyCardsDPS + pupSkinsDPS + pupItemsRealDPS
