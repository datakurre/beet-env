from beet import Advancement
from beet import Blockstate
from beet import Context
from beet import Function
from beet import LootTable
from beet import Model
from pathlib import Path
from pydantic import BaseModel
from typing import Dict
from yaml import safe_load
from functools import lru_cache
import json
import re


package = Path(__file__).parent / "data" / "blocks"


class Block(BaseModel):
    id: int
    name: str
    slot: str
    faces: Dict[str, str]


@lru_cache()
def snake_case(name: str) -> str:
    return re.sub(r"[_]+", "_", re.sub(r"[^a-zA-Z]", "_", name)).strip("_").lower()


def beet_default(ctx: Context):
    blocks = [
        Block(**item) for item in safe_load((ctx.directory / "blocks.yaml").read_text())
    ]
    for config in blocks:
        block, state = config.slot.strip("]").split("[")
        ctx.assets[f"minecraft:block/{snake_case(config.name)}"] = Model(
            {
                "parent": "block/cube_all",
                "textures": {
                    "all": config.faces.get("up"),
                    "up": config.faces.get("up"),
                    "down": config.faces.get("up"),
                    "north": config.faces.get("up"),
                    "east": config.faces.get("up"),
                    "south": config.faces.get("up"),
                    "west": config.faces.get("up"),
                }
                | {key: face for key, face in config.faces.items()},
                "elements": [
                    {
                        "from": [0, 0, 0],
                        "to": [16, 16, 16],
                        "faces": {
                            key: {"texture": f"#{key}", "cullface": key}
                            for key in config.faces
                        },
                    }
                ],
            }
        )
        ctx.assets[f"minecraft:{block}"] = Blockstate(
            {
                "variants": {
                    state: [{"model": f"minecraft:block/{snake_case(config.name)}"}],
                }
            }
        )
        ctx.data[f"minecraft:blocks/{block}"] = LootTable(
            {
                "pools": [
                    {
                        "rolls": 1,
                        "entries": [
                            {
                                "type": "minecraft:item",
                                "name": "minecraft:player_head",
                                "functions": [
                                    {
                                        "function": "minecraft:set_components",
                                        "components": {
                                            "minecraft:custom_model_data": 90100,
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                    {
                        "rolls": 1,
                        "entries": [
                            {
                                "type": "minecraft:item",
                                "name": "minecraft:barrier",
                                "functions": [
                                    {
                                        "function": "minecraft:set_components",
                                        "components": {
                                            "minecraft:custom_model_data": config.id,
                                            "minecraft:custom_name": json.dumps(
                                                {
                                                    "text": config.name,
                                                    "italic": False,
                                                    "color": "white",
                                                }
                                            ),
                                        },
                                    }
                                ],
                            }
                        ],
                    },
                ]
            }
        )
    ctx.assets["minecraft:item/barrier"] = Model(
        {
            "parent": "item/generated",
            "textures": {
                "layer0": "block:bedrock",
            },
            "overrides": [
                {
                    "predicate": {"custom_model_data": config.id},
                    "model": f"block/{snake_case(config.name)}",
                }
                for config in blocks
            ],
        }
    )
    ctx.data["blocks:load"] = Function(
        (package / "function" / "load.mcfunction").read_text(),
        tags=["minecraft:load"],
    )
    ctx.data["blocks:main"] = Function(
        (package / "function" / "main.mcfunction").read_text(),
        tags=["minecraft:tick"],
    )
    ctx.data["blocks:place_block/trigger"] = Advancement(
        {
            "criteria": {
                "requirement": {
                    "trigger": "minecraft:placed_block",
                    "conditions": {
                        "location": [
                            {
                                "condition": "minecraft:block_state_property",
                                "block": "minecraft:barrier",
                                "properties": {},
                            }
                        ]
                    },
                }
            },
            "rewards": {"function": "blocks:place_trigger"},
        }
    )
