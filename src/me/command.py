from __future__ import annotations

from typing import Any

from cachetools import cached
from cachetools.ttl import TTLCache
from discord.embeds import Embed
from discord.utils import cached_property

from ..lib.redis import r


def ME(author: cached_property | Any):
    e = Embed()

    if not r.exists(f"_id_{author.id}"):
        e.title = "Who are you?"
        e.description = "You are not registered. Please register and try again."
        return e

    d = r.hgetall(f"_id_{author.id}")
    _waxid = d["wallet"]
    _verified = d["verified"]
    _type = d["type"]

    _provider = ""
    if _type == "wax-cloud":
        _provider = "Wax Cloud Wallet"
    elif _type == "anchor":
        _provider = "Anchor"
    elif _type == "scatter":
        _provider = "Scatter"

    _v_title = "❌" if _verified == "False" else "✅"

    e.title = "Profile | World of Cryptopups"
    e.set_author(name=author.display_name, icon_url=author.avatar_url)
    e.add_field(name="💳 WAX Wallet", value=_waxid, inline=True)
    e.add_field(name="👥 Account Provider", value=_provider, inline=False)
    e.add_field(name=f"{_v_title} Verified", value=_verified, inline=False)
    return e
