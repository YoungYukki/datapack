import questionary, shutil
from pathlib import Path
from utils.store import STORE
from utils.io import (
    read_json,
)
from utils import (
    console,
    format_count,
    concat,
    cut_minecraft,
    pick_datapack,
    pick_draft,
)


def main():
    draft_path = pick_draft()
    datapack_directory = pick_datapack()
    data_path = Path("pack") / "data"
    datapack_data_path = datapack_directory / "data"
    # 选择namespace;如果默认namespace在选项里面就抬到首位;如果没有设置namespace就设置默认选项
    namespaces = [namespace.name for namespace in data_path.glob("*")]
    if STORE.DEFAULT.NAMESPACE in namespaces:
        namespaces.remove(STORE.DEFAULT.NAMESPACE)
        namespaces.insert(0, STORE.DEFAULT.NAMESPACE)
    namespace = questionary.select("选择namespce", choices=namespaces).ask()
    console.info(namespace)
    if not STORE.DEFAULT.NAMESPACE:
        STORE.DEFAULT.update("namespace", namespace)
    # 配方出目录
    recipe_dir = data_path / namespace / "recipe"
    if not copy(draft_path, recipe_dir):
        return None
    datapack_recipe_dir = datapack_data_path / namespace / "recipe"
    if not copy(draft_path, datapack_recipe_dir):
        return None
    Path(draft_path).unlink()


def read_draft(path: str) -> dict | None:
    draft: dict = read_json(path)
    if not "type" in draft.keys():
        console.danger("没有<type>键")
        return dict()
    _type = draft.get("type")
    if not _type in STORE.STATIC.RECIPES:
        console.danger("没有此配方生成器类型")
        return dict()
    return draft


def copy(draft_path: str, recipe_dir: Path):
    # 读取draft
    draft = read_draft(draft_path)
    if not draft:
        return None
    # 新建文件名
    name = build_name(draft)
    if not name:
        return None
    recipe_path: Path = recipe_dir / draft.get("type")[10:] / name
    console.info(f"{draft_path} => {recipe_path}")
    if recipe_path.exists():
        console.danger("已经存在")
        return None
    is_copy = questionary.confirm("确定移动?").ask()
    if not is_copy:
        console.danger("取消移动")
        return None
    shutil.copy(draft_path, recipe_path)
    if not recipe_path.exists():
        console.danger("复制失败")
        return None
    console.success("复制成功")


def build_name(draft: dict) -> str:
    _type = draft.get("type")
    if _type in STORE.STATIC.INGREDIENT:
        ingredient = draft.get("ingredient")
        leading_part = ingredient_part(ingredient)
    elif _type in STORE.STATIC.INGREDIENTS:
        ingredients = draft.get("ingredients")
        leading_part = ingredients_part(ingredients)
    else:
        console.danger("未知的类型")
        return str()
    result = draft.get("result")
    return f"{leading_part}={result_part(result)}.json"


def ingredients_part(ingredients: list) -> str:
    return concat("+", [f"{ingredient_part(ingredient)}" for ingredient in ingredients])


def ingredient_part(ingredient: list | str) -> str:
    if isinstance(ingredient, str):
        return f"[{cut_minecraft(ingredient)}]"
    return f'[{concat("~", ingredient)}]'


def result_part(result: dict | str) -> str:
    if isinstance(result, str):
        return result
    _id = result.get("id")
    if "count" in result.keys():
        _count = result.get("count")
    else:
        _count = ""
    return f"{format_count(_count)}[{cut_minecraft(_id)}]"
