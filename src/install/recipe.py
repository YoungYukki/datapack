import json
from pathlib import Path
from utils.store import STORE
from utils import (
    pick_file,
    format_count,
    concat,
    console,
)


def main():
    if not STORE.DEFAULT.DOWNLOAD_PATH:
        console.warning("默认下载地址不存在")
        draft_path = pick_file()
        STORE.DEFAULT.update("download_directory", Path(draft_path).parent)
    if not draft_path:
        console.danger("没有选择文件")
        return None
    draft = read_draft(draft_path)
    if not draft:
        return None
    copy(draft, draft_path)


def read_draft(path: str) -> dict | None:
    with open(path, "r", encoding="utf-8") as f:
        draft: dict = json.load(f)
    if not "type" in draft.keys():
        console.danger("没有<type>键")
        return dict()
    _type = draft.get("type")
    if not _type in STORE.STATIC.RECIPES:
        console.danger("没有此配方生成器类型")
        return dict()
    return draft


def copy(draft: dict, draft_path: str):
    new_name = build_new_name(draft)
    console.info(new_name)

    # data_path = Path("data")
    # namespaces = [namespace.name for namespace in data_path.glob("*")]
    # namespace = questionary.select("选择namespace", choices=namespaces).ask()
    # recipe_path: Path = data_path / namespace / "recipe" / _type / new_name
    # print(f"{draft_path} => {recipe_path}")
    # is_copy = questionary.confirm("确定复制?").ask()
    # if not is_copy:
    #     return None
    # shutil.copy(draft_path, recipe_path)
    # commit(recipe_path, new_name)
    # Path(draft_path).unlink()


def build_new_name(draft: dict) -> str:
    _type = draft.get("type")
    if _type in STORE.STATIC.INGREDIENT:
        ingredient = draft.get("ingredient")
        leading_part = ingredient_part(ingredient)
    elif _type in STORE.STATIC.INGREDIENTS:
        ingredients = draft.get("ingredients")
        leading_part = ingredients_part(ingredients)
    else:
        console.danger("未知的类型")
    result = draft.get("result")
    return f"{leading_part}={result_part(result)}.json"


def ingredients_part(ingredients: list) -> str:
    return concat("+", [ingredient_part(ingredient) for ingredient in ingredients])


def ingredient_part(ingredient: list | str) -> str:
    if isinstance(ingredient, str):
        return ingredient[10:]
    return concat("~", ingredient)


def result_part(result: dict | str) -> str:
    if isinstance(result, str):
        return result
    _id = result.get("id")
    if "count" in result.keys():
        _count = result.get("count")
    else:
        _count = ""
    return f"{format_count(_count)}{_id[10:]}"
