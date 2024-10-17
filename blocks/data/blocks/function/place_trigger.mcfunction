# This replaces any matching barrier with custom block within seven (7) blocks of the current player position
from beet import Function
from dataclasses import dataclass
from functools import lru_cache
from pydantic import BaseModel
from yaml import safe_load

import re


@lru_cache()
def snake_case(name: str) -> str:
    return re.sub(r"[_]+", "_", re.sub(r"[^a-zA-Z]", "_", name)).strip("_").lower()


class Block(BaseModel):
    id: int
    name: str
    slot: str


for item in safe_load((ctx.directory / "blocks.yaml").read_text()):
    block = Block(**item)
    function ~/{snake_case(block.name)}:
        for i in range(-7, 8):
                execute at @s positioned ~ ~i ~ run
                        fill ~-7 ~ ~-7 ~7 ~ ~7 block.slot replace barrier
    execute if score @s heldItem matches block.id run function ~/{snake_case(block.name)}