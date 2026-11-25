import questionary
from pathlib import Path
from utils.store import STORE
from install.recipe import main as recipe
from utils.sync import main as sync
from utils import pick_datapack


def datapack_install():
    generator = questionary.select(
        "选择生成器:",
        choices=STORE.STATIC.GENERATORS,
    ).ask()
    match generator:
        case "recipe":
            recipe()
        case _:
            print("没有选择生成器")


def datapack_sync():
    # 选择数据包目录;检测是不是数据包;如果默认目录和现在选择的不一样则更新
    datapack_directory = pick_datapack()
    sync(previous_dir=Path("pack"), updated_dir=datapack_directory)
