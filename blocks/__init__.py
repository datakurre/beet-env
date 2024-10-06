from beet import Blockstate
from beet import Context
from beet import Function
from beet import LootTable
from beet import Model
from pathlib import Path


package = Path(__file__).parent / "data" / "blocks"


def beet_default(ctx: Context):
    ctx.assets["minecraft:block/dice"] = Model(
        {
            "parent": "block/cube_all",
            "textures": {
                "one": "minecraft:block/dice/1",
                "two": "minecraft:block/dice/2",
                "three": "minecraft:block/dice/3",
                "four": "minecraft:block/dice/4",
                "five": "minecraft:block/dice/5",
                "six": "minecraft:block/dice/6",
                "all": "minecraft:block/dice/6",
            },
            "elements": [
                {
                    "from": [0, 0, 0],
                    "to": [16, 16, 16],
                    "faces": {
                        "down": {"texture": "#one", "cullface": "down"},
                        "up": {"texture": "#six", "cullface": "up"},
                        "north": {"texture": "#three", "cullface": "north"},
                        "south": {"texture": "#four", "cullface": "south"},
                        "west": {"texture": "#five", "cullface": "west"},
                        "east": {"texture": "#two", "cullface": "east"},
                    },
                }
            ],
        }
    )
    ctx.assets["minecraft:oak_slab"] = Blockstate(
        {
            "variants": {
                "type=double,waterlogged=true": [{"model": "minecraft:block/dice"}],
            }
        }
    )
    ctx.data["minecraft:blocks/oak_slab"] = LootTable(
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
                                        "minecraft:custom_model_data": 90101,
                                    },
                                }
                            ],
                        }
                    ],
                },
            ]
        }
    )
    ctx.data["blocks:load"] = Function(
        (package / "function" / "load.mcfunction").read_text(), tags=["minecraft:load"]
    )
    ctx.data["blocks:main"] = Function(
        (package / "function" / "main.mcfunction").read_text(), tags=["minecraft:tick"]
    )
    ctx.assets["minecraft:item/barrier"] = Model(
        {
            "parent": "item/generated",
            "textures": {
                "layer0": "block:bedrock",
            },
            "overrides": [
                {"predicate": {"custom_model_data": 90101}, "model": "block/dice"}
            ],
        }
    )
