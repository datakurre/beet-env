# This replaces any matching barrier with custom block within seven (7) blocks of the current player position
from beet import Function
from dataclasses import dataclass
from yaml import safe_load

from blocks.utils import get_blocks


for block in get_blocks(ctx):
    function ~/{block.key}:
        for i in range(-7, 8):
                execute at @s positioned ~ ~i ~ run
                        fill ~-7 ~ ~-7 ~7 ~ ~7 block.slot replace barrier
    execute if score @s heldItem matches block.id run function ~/{block.key}