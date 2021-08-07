from __future__ import annotations

from typing import Any

from cachetools import TTLCache, cached
from discord import Embed
from discord.utils import cached_property
from src.lib.pups import SCHEMAS
from src.lib.redis import r

from .dps import calculateDPS, calculateItemsDPS, getSeasonPassDPS
from .request import (
    PUPITEMS_API,
    PUPPYCARDS_API,
    PUPSKINS_API,
    _urls,
    calculator,
    requester,
)


# base dps calculation command
# @cached(cache=TTLCache(maxsize=128, ttl=300))
def ROLL(owner: str, author: cached_property | Any, auth: bool, seasonDPS: str | None):
    """
    `>roll` command
    """

    resps = calculator(owner)

    puppyCardsData = []
    pupSkinsData = []
    pupItemsData = []

    for i in resps:
        if i["schema"] == SCHEMAS[1]:
            puppyCardsData = i["values"]
        if i["schema"] == SCHEMAS[0]:
            pupSkinsData = i["values"]
        if i["schema"] == SCHEMAS[2]:
            pupItemsData = i["values"]

    # if not puppyCardsData or not pupSkinsData or not pupItemsData:
    #     # if failed request, return this
    #     return Embed(
    #         title="Request Failed",
    #         description="Failed to fetch! Is your WAX ID correct?",
    #     )

    # calculate all dps
    puppyCardsDPS = calculateDPS(owner, puppyCardsData)
    pupSkinsDPS = calculateDPS(owner, pupSkinsData)
    pupItemsDPS = calculateDPS(owner, pupItemsData)
    pupItemsRealDPS = calculateItemsDPS(pupSkinsData, pupItemsData, owner)

    totalDPS = puppyCardsDPS + pupSkinsDPS + pupItemsRealDPS

    # set final message
    e = Embed(title=f"**{owner}** | DPS Calculator")
    e.set_author(name=author.display_name, icon_url=author.avatar_url)
    e.set_thumbnail(url=author.avatar_url)
    e.add_field(
        name="🎴 Puppy Cards", value="{:,} DPS".format(puppyCardsDPS), inline=True
    )
    e.add_field(name="🃏 Pup Skins", value="{:,} DPS".format(pupSkinsDPS), inline=True)
    e.add_field(
        name="⚔️ Pup Items (Raw)",
        value="{:,} DPS".format(pupItemsDPS),
        inline=True,
    )
    e.add_field(
        name="⚔️ Pup Items (Real)",
        value="{:,} DPS".format(pupItemsRealDPS),
        inline=True,
    )

    e.add_field(name="\u200b", value="\u200b", inline=False)
    e.add_field(name="🗡 TOTAL DPS", value="**{:,}**".format(totalDPS), inline=False)

    # special (TRUE DPS) calculation
    if not seasonDPS:
        seasonDPS = str(getSeasonPassDPS(owner))
        if auth:
            r.hset(f"_id_{author.id}", "seasonDPS", seasonDPS)

    e.add_field(
        name="🛡 SEASON PASS DPS", value="**{:,}**".format(int(seasonDPS)), inline=False
    )

    e.set_footer(text="All Rights Reserved | World of Cryptopups")

    return e
