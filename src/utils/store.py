import yaml
from pathlib import Path
from utils import console


class Default:
    PATH = "default.yaml"
    DOWNLOAD_PATH = None
    DATAPACK_PATH = None

    def __init__(self):
        if not Path(self.PATH).exists():
            console.danger("不存在默认配置")
            return None
        with open(self.PATH, "r", encoding="utf-8") as f:
            default: dict = yaml.safe_load(f)
        self.DOWNLOAD_PATH = default.get("download_path")
        self.DATAPACK_PATH = default.get("datapack_path")


class Stataic:
    GENERATORS = [
        "recipe",
    ]
    RECIPE = [
        "minecraft:blasting",
        "minecraft:crafting_shaped",
        "minecraft:crafting_shapeless",
        "minecraft:smelting",
        "minecraft:smoking",
        "minecraft:stonecutting",
    ]


class Store:
    STATIC = Stataic()
    DEFAULT = Default()


STORE = Store()
