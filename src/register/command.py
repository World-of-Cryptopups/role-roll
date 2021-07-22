from __future__ import annotations

from typing import Any

from discord.utils import cached_property
from src.roll.dps import getTrueDPS

from ..lib.redis import r


def REGISTER(token: str, author: cached_property | Any):
    # id exists
    if r.exists(f"_id_{author.id}") == 1:
        return f"❗️ You have registered already an account! If you want to change your **WAX ID** please contact an admin."

    # token already exists
    if r.exists(token) == 0:
        return f"⚠️ This token is not valid. Please contact an admin on how to get a valid token."

    # get wax id from data
    _d = r.hgetall(token)

    # fetch the true DPS upon register
    _trueDPS = getTrueDPS(_d["wallet"])

    # register key
    r.hset(
        name=f"_id_{author.id}",
        mapping={
            "wallet": _d["wallet"],
            "type": _d["type"],
            "verified": str(True),
            "trueDPS": str(_trueDPS),
        },
    )
    return f"✅ <@!{author.id}>, You successfully registered. You can check your status with the command `>me`"
