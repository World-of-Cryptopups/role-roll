from __future__ import annotations

from typing import Any

from discord.utils import cached_property
from src.roll.dps import getSeasonPassDPS

from ..lib.redis import r
from ..roll.command import ROLL


def DPS(author: cached_property | Any):
    """
    >dps command
    """

    _id = f"_id_{author.id}"

    # get all keys
    d = r.hgetall(_id)

    _owner = d["wallet"]
    if not _owner:
        return f"<@!{author.id}> Your `wallet` is not currently registered or saved. Please contact an admin to fix this issue."

    return ROLL(_owner, author, True, d.get("seasonDPS"))
