import questionary, shutil
from pathlib import Path
from utils.store import STORE
from utils.io import (
    pick_file,
    pick_folder,
    read_json,
)
from utils import (
    format_count,
    concat,
    cut_minecraft,
    console,
)


def main():
    # 选择draft文件位置;如果没有默认下载地址就更新;
    draft_path = pick_file(STORE.DEFAULT.DOWNLOAD_DIRECTORY)
    if not draft_path:
        console.danger("没有选择文件")
        return None
    if not STORE.DEFAULT.DOWNLOAD_DIRECTORY:
        console.warning("默认DOWNLOAD_DIRECTORY不存在")
        STORE.DEFAULT.update(
            "download_directory",
            str(Path(draft_path).parent),
        )
    # 获取数据包目录;如果默认目录不存在,就设置默认目录
    datapack_directory = pick_folder(STORE.DEFAULT.DATAPACK_DIRECTORY)
    if not STORE.DEFAULT.DATAPACK_DIRECTORY:
        console.info("默认DATAPACK_DIRECTORY不存在")
        STORE.DEFAULT.update(
            "datapack_directory",
            datapack_directory,
        )
    data_path = Path(datapack_directory) / "data"
    mcmeta = Path(datapack_directory) / "pack.mcmeta"
    if not mcmeta.exists():
        console.danger(f"{data_path}不是数据包")
        return None
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
    copy(draft_path, recipe_dir)


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
    recipe_path = recipe_dir / draft.get("type")[10:] / name
    console.info(f"{draft_path} => {recipe_path}")
    if draft_path == recipe_path:
        console.warning("文件地址一样")
        return None
    is_copy = questionary.confirm("确定移动?").ask()
    if not is_copy:
        console.warning("取消移动")
        return None
    shutil.move(draft_path, recipe_path)


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
