import tkinter as tk
from tkinter import filedialog
import shutil
import json
from pathlib import Path
from collections import Counter
import questionary
import subprocess

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


def main():
    generator = questionary.select("选择生成器:", choices=GENERATORS).ask()
    match generator:
        case "recipe":
            recipe()
        case _:
            print("没有选择生成器")


def recipe():
    draft_path = pick_file()
    if not draft_path:
        print("没有选择文件")
        return None
    draft = read_draft(draft_path)
    if not draft:
        return None
    recipe_copy(draft, draft_path)


def pick_file(title="选择文件", types=[("所有文件", "*.*")]):
    tk.Tk().withdraw()
    return filedialog.askopenfilename(title=title, filetypes=types)


def read_draft(path: str) -> dict | None:
    with open(path, "r", encoding="utf-8") as f:
        draft: dict = json.load(f)
    if not "type" in draft.keys():
        print("没有<type>键")
        return None
    _type = draft.get("type")
    if not _type in RECIPE:
        print("没有此配方生成器类型")
        return None
    return draft


def recipe_copy(draft: dict, draft_path: str):
    new_name = create_new_name(draft)
    _type = draft.get("type")[10:]
    data_path = Path("data")
    namespaces = [namespace.name for namespace in data_path.glob("*")]
    namespace = questionary.select("选择namespace", choices=namespaces).ask()
    recipe_path: Path = data_path / namespace / "recipe" / _type / new_name
    print(f"{draft_path} => {recipe_path}")
    is_copy = questionary.confirm("确定复制?").ask()
    if not is_copy:
        return None
    shutil.copy(draft_path, recipe_path)
    commit(recipe_path, new_name)


def create_new_name(draft: dict) -> Path:
    ingredient = draft.get("ingredient")
    result = draft.get("result")
    return f"{leading_part(ingredient)}__{trailing_part(result)}.json"


def leading_part(ingredient: str | list) -> str:
    if isinstance(ingredient, str):
        return ingredient[10:]
    result: dict = Counter(ingredient)
    return "_".join(f"{_count}-{_id[10:]}" for _id, _count in result.items())


def trailing_part(result: dict) -> str:
    _id = result.get("id")
    if "count" in result.keys():
        _count = result.get("count")
    else:
        _count = ""
    return f"{_count}-{_id[10:]}"


def commit(path: str, message: str):
    subprocess.run(["git", "add", path])
    subprocess.run(["git", "commit", "-m", message])


if __name__ == "__main__":
    main()
