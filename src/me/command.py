from __future__ import annotations

from typing import Any

from discord.embeds import Embed
from discord.utils import cached_property

from ..lib.redis import r


async def ME(author: cached_property | Any):
    e = Embed()

    if not r.exists(author.id):
        e.title = "Who are you?"
        e.description = "You are not registered. Please register and try again."
        return e

    d = r.hgetall(author.id)
    _waxid = d["wax_id"]
    _verified = d["verified"]

    _v_title = "❌" if _verified == "False" else "✅"

    e.title = "Profile | World of Cryptopups"
    e.set_author(name=author.display_name, icon_url=author.avatar_url)
    e.add_field(name="💹 Wax ID", value=_waxid, inline=False)
    e.add_field(name=f"{_v_title} Verified", value=_verified, inline=False)
    return e
