from install.recipe import copy
from pathlib import Path

def main():
    pass

def recipe():
    work_directory = Path(
        r"D:\Minecraft\hmcl\.minecraft\versions\26.1.2\saves\26_1_2\datapacks\youngyukki-datapack\data\youngyukki\recipe"
    )
    _recipes = work_directory.rglob('*.json')
    for _recipe in _recipes:
        copy(_recipe, work_directory)

if __name__ == '__main__':
    recipe()