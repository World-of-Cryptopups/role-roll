from __future__ import annotations

from typing import Any

from cachetools import cached
from cachetools.ttl import TTLCache
from discord.embeds import Embed
from discord.utils import cached_property

from ..lib.redis import r


# cache database response for 10 minutes
@cached(cache=TTLCache(maxsize=128, ttl=10))
def ME(author: cached_property | Any):
    # fetch all keys of id
    d = r.hgetall(f"_id_{author.id}")

    _waxid = d["wallet"]
    _verified = d["verified"]
    _type = d["type"]
    _seasonDPS = d.get("seasonDPS")

    _provider = ""
    if _type == "wax-cloud":
        _provider = "Wax Cloud Wallet"
    elif _type == "anchor":
        _provider = "Anchor"
    elif _type == "scatter":
        _provider = "Scatter"

    _v_title = "❌" if _verified == "False" else "✅"

    e = Embed()
    e.title = "Profile | World of Cryptopups"
    e.set_author(name=author.display_name, icon_url=author.avatar_url)
    e.add_field(name="💳 WAX Wallet", value=_waxid, inline=False)
    e.add_field(name="👥 Account Provider", value=_provider, inline=True)
    e.add_field(name=f"{_v_title} Verified", value=_verified, inline=True)

    if _seasonDPS:
        e.add_field(
            name="🛡 SEASON PASS DPS",
            value="**{:,}**".format(int(_seasonDPS)),
            inline=False,
        )

    return e
