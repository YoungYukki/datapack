from collections import Counter
from pathlib import Path
from utils import (
    console,
)
from utils.io import pick_folder, pick_file
from utils.store import STORE


def format_count(count: int) -> str:
    if count == 1:
        return ""
    return f"{count}"


def cut_minecraft(entry: str):
    sep = "minecraft:"
    _, found, rest = entry.partition(sep)
    if found == "":
        return entry
    return rest


def concat(joiner: str, iterable: list) -> str:
    result: dict = Counter(iterable)
    return joiner.join(
        f"{format_count(count)}{cut_minecraft(entry)}"
        for entry, count in result.items()
    )


def check_datapack(dir: str) -> bool:
    mcmeta_path = Path(dir) / "pack.mcmeta"
    return mcmeta_path.exists()


# 选择数据包目录;检测是不是数据包;如果默认目录和现在选择的不一样则更新
def pick_datapack() -> Path:
    datapack_directory = pick_folder(
        STORE.DEFAULT.DATAPACK_DIRECTORY, title="选择数据包目录"
    )
    if not datapack_directory:
        console.danger("没有选择数据包目录")
        return None
    if not check_datapack(datapack_directory):
        console.danger(f"{datapack_directory}不是数据包")
        return None
    if not datapack_directory == STORE.DEFAULT.DATAPACK_DIRECTORY:
        console.warning("更新默认数据包位置")
        STORE.DEFAULT.update("datapack_directory", datapack_directory)
    return Path(datapack_directory)


# 选择draft文件位置;如果默认下载地址和现在不一样则更新;
def pick_draft() -> Path:
    draft_path = pick_file(STORE.DEFAULT.DOWNLOAD_DIRECTORY, title="选择draft")
    if not draft_path:
        console.danger("没有选择文件")
        return None
    download_directory = str(Path(draft_path).parent)
    if not download_directory == STORE.DEFAULT.DOWNLOAD_DIRECTORY:
        console.warning("更新默认下载目录位置")
        STORE.DEFAULT.update(
            "download_directory",
            download_directory,
        )
    return Path(draft_path)
