# from pathlib import Path
# import shutil
# from utils import console
# from utils.io import pick_folder


# def main():
#     current_dir = Path(pick_folder())
#     back_dir = Path("pack")
#     sync(current_dir=current_dir, back_dir=back_dir)


# def sync(back_dir: Path, target_dir: Path):
#     items = current_dir.rglob("*")
#     for item in items:
#         if item.is_dir(): 
#             sync(current_dir=item, back_dir=back_dir / item.name)
#         else:
#             copy(item, back_dir)


# def copy(current_path: Path, back_dir: Path):
#     back_path = back_dir / current_path.name
#     console.info(f"{current_path} => {back_path}")
