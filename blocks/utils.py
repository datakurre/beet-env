from beet import Context
from functools import lru_cache
from pydantic import BaseModel
from pydantic import FilePath
from pydantic import model_validator
from typing import Any
from typing import Dict
from typing import List
from yaml import safe_load
import re


class Block(BaseModel):
    id: int
    key: str
    name: str
    slot: str
    faces: Dict[str, str]

    @model_validator(mode="before")
    @classmethod
    def interpolate(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        data["key"] = snake_case(data["name"]) if data.get("name") else None
        return data


@lru_cache()
def snake_case(name: str) -> str:
    return re.sub(r"[_]+", "_", re.sub(r"[^a-zA-Z]", "_", name)).strip("_").lower()


@lru_cache()
def load_blocks(path: FilePath) -> List[Block]:
    return [Block(**item) for item in safe_load(path.read_text())]


def get_blocks(ctx: Context) -> List[Block]:
    return load_blocks(
        ctx.directory / ((ctx.meta.get("blocks") or {}).get("data") or "blocks.yaml")
    )
