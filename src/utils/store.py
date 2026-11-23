import yaml
from pathlib import Path
from utils import console


class Default:
    PATH = "default.yaml"
    DOWNLOAD_PATH = None
    DATAPACK_PATH = None
    _default = {}

    def __init__(self):
        if not Path(self.PATH).exists():
            console.danger("默认配置文件不存在")
            return None
        with open(self.PATH, "r", encoding="utf-8") as f:
            self._default = yaml.safe_load(f)
        self.DOWNLOAD_DIRECTORY = self._default.get("download_directory")
        self.DATAPACK_DIRECTORY = self._default.get("datapack_directory")

    def update(self, key: str, value: str):
        if not key in self._default.keys():
            console.danger("不存在的default键值")
            return None
        self._default.update({key: value})
        with open(self.PATH, "w", encoding="utf-8") as f:
            f.write(yaml.safe_dump(self._default))


class Stataic:
    GENERATORS = [
        "recipe",
    ]
    INGREDIENT = [
        "minecraft:blasting",
        "minecraft:smelting",
        "minecraft:smoking",
        "minecraft:stonecutting",
    ]
    INGREDIENTS = [
        "minecraft:crafting_shapeless",
    ]

    def __init__(self):
        self.RECIPES = self.INGREDIENT + self.INGREDIENTS


class Store:
    STATIC = Stataic()
    DEFAULT = Default()


STORE = Store()
