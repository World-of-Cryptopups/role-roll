from __future__ import annotations

from typing import Any

from discord.utils import cached_property

from ..lib.redis import r


async def REGISTER(owner: str, author: cached_property | Any):
    if r.exists(owner) == 1:
        return f"❗️ Wax ID: **`{owner}`** has already been registered. Please contact an admin if you did not register this account."

    r.hset(
        name=owner,
        mapping={
            "discord_id": author.id,
            "verified": str(False),
        },
    )
    return f"✅ Wax ID: **`{owner}`** is successfully registered by <@!{author.id}>"
