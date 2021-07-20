from __future__ import annotations

from typing import Any

from discord.utils import cached_property

from ..lib.redis import r


async def REGISTER(owner: str, author: cached_property | Any):
    # id exists
    if r.exists(author.id) == 1:
        return f"❗️ You have registered already an account! If you want to change please contact an admin."

    # token exists in list
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
