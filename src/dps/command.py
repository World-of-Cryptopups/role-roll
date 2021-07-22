from __future__ import annotations

from typing import Any

from discord.utils import cached_property

from ..lib.redis import r
from ..roll.command import ROLL


def DPS(author: cached_property | Any):
    """
    >dps command
    """

    if r.exists(f"_id_{author.id}") == 0:
        return "You are not currently registered. Please register with the `>register` command and try again."

    _owner = r.hget(f"_id_{author.id}", "wallet")
    if not _owner:
        return f"<@!{author.id}> Your `wallet` is not currently registered or saved. Please contact an admin to fix this issue."

    return ROLL(_owner, author)
