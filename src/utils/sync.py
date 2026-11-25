import shutil
from pathlib import Path
from utils import console


def main(previous_dir: Path, updated_dir: Path):
    clone(previous_dir, updated_dir)
    delete(previous_dir, updated_dir)


def clone(previous_dir: Path, updated_dir: Path):
    items = previous_dir.glob("*")
    for item in items:
        if item.is_dir():
            clone(previous_dir=item, updated_dir=Path(updated_dir) / item.name)
        else:
            copy(item, Path(updated_dir))


def copy(previous_path: Path, updated_dir: Path):
    updated_path = updated_dir / previous_path.name
    if updated_path.exists():
        console.info(f"{updated_path}已经存在")
        return None
    if not updated_dir.exists():
        console.warning(f"{updated_dir}不存在")
        updated_dir.mkdir(parents=True, exist_ok=True)
    if not updated_dir.exists():
        console.danger(f"{updated_dir}创建失败")
        return None
    console.info(f"{previous_path} => {updated_path}")
    shutil.copy(previous_path, updated_path)
    if not updated_path.exists():
        console.danger(f"{updated_path}复制失败")
        return None
    console.success(f"{updated_path}复制成功")


def delete(previous_dir: Path, updated_dir: Path):
    items = Path(updated_dir).glob("*")
    for item in items:
        if item.is_dir():
            delete(updated_dir=item, previous_dir=Path(previous_dir) / item.name)
        else:
            remove(item, Path(previous_dir))


def remove(updated_path: Path, previous_dir: Path):
    preivous_path = previous_dir / updated_path.name
    if preivous_path.exists():
        console.info(f"{updated_path} == {preivous_path}")
        return None
    console.warning(f"{updated_path} != {preivous_path}")
    updated_path.unlink()
    if updated_path.exists():
        console.danger(f"{updated_path}删除失败")
        return None
    console.success(f"{updated_path}删除成功")
