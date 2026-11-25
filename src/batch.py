from install.recipe import copy
from pathlib import Path


def main():
    recipe()


def recipe():
    work_directory = Path(r"pack\data\youngyukki\recipe")
    _recipes = work_directory.rglob("*.json")
    for _recipe in _recipes:
        copy(_recipe, work_directory)


if __name__ == "__main__":
    recipe()
