from beet import Advancement
from beet import Blockstate
from beet import Context
from beet import Function
from beet import LootTable
from beet import Model
from blocks.utils import get_blocks
from pathlib import Path
import json


package = Path(__file__).parent / "data" / "blocks"


def beet_default(ctx: Context):
    for config in get_blocks(ctx):
        block, state = config.slot.strip("]").split("[")
        ctx.assets[f"minecraft:block/{config.key}"] = Model(
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
                    state: [{"model": f"minecraft:block/{config.key}"}],
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
                    "model": f"block/{config.key}",
                }
                for config in get_blocks(ctx)
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
