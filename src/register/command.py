from __future__ import annotations

from typing import Any

from discord.utils import cached_property

from ..lib.redis import r


async def REGISTER(token: str, author: cached_property | Any):
    # id exists
    if r.exists(f"_id_{author.id}") == 1:
        return f"❗️ You have registered already an account! If you want to change your **WAX ID** please contact an admin."

    # token already exists
    if r.exists(token) == 0:
        return f"⚠️ This token is not valid. Please contact an admin on how to get a valid token."

    # get wax id from data
    _d = r.hgetall(token)

    # register key
    r.hset(
        name=f"_id_{author.id}",
        mapping={
            "wallet": _d["wallet"],
            "type": _d["type"],
            "verified": str(True),
        },
    )
    return f"✅ <@!{author.id}>, You successfully registered. You can check your status with the command `>me`"
