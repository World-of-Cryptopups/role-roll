from __future__ import annotations

from typing import Any

from discord.utils import cached_property
from src.roll.dps import getSeasonPassDPS

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
    _seasonDPS = getSeasonPassDPS(_d["wallet"])

    # register id to set
    r.sadd("_registered_ids", f"_id_{author.id}")

    # register key
    r.hset(
        name=f"_id_{author.id}",
        mapping={
            "wallet": _d["wallet"],  # get the wllaet
            "type": _d["type"],  # get also the type
            "verified": str(True),  # verify it
            "seasonDPS": str(_seasonDPS),  # get the seasonDPS
            "avatarUrl": author.avatar_url,  # get the author profile image / avatar url
        },
    )
    return f"✅ <@!{author.id}>, You successfully registered. You can check your status with the command `>me`"
