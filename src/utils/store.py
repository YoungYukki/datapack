import yaml
from pathlib import Path
from utils import console
from utils.io import (
    read_yaml,
    write_yaml,
)


class Default:
    PATH = "default.yaml"
    DEFAULT_KEY = [
        "download_directory",
        "datapack_directory",
        "namespace",
    ]

    def __init__(self):
        if not Path(self.PATH).exists():
            console.warning("默认配置文件不存在")
            write_yaml(self.PATH, {key: "" for key in self.DEFAULT_KEY})
        self._default: dict = read_yaml(self.PATH)
        self.DOWNLOAD_DIRECTORY = self._default.get("download_directory")
        self.DATAPACK_DIRECTORY = self._default.get("datapack_directory")
        self.NAMESPACE = self._default.get("namespace")

    def update(self, key: str, value: str):
        if not key in self._default.keys():
            console.warning(f"不存在{key}")
        self._default.update({key: value})
        write_yaml(self.PATH, self._default)


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
