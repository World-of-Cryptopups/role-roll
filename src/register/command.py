from __future__ import annotations

from typing import Any

from discord.utils import cached_property

from ..lib.redis import r


async def REGISTER(owner: str, author: cached_property | Any):
    # exists in set
    if r.sismember("_tokens_list", owner):
        return f"❗️ Wax ID: **`{owner}`** was already registed. Please contact an admin if you did not register this account."

    # register waxid to set
    r.sadd("_tokens_list", owner)

    # register key
    r.hset(
        name=author.id,
        mapping={
            "wax_id": owner,
            "verified": str(False),
        },
    )
    return f"✅ Wax ID: **`{owner}`** is successfully registered by <@!{author.id}>"
