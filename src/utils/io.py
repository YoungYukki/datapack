import yaml, json
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from utils import console


def read_yaml(path: str | Path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def write_yaml(path: str | Path, params):
    with open(path, "w", encoding="utf-8") as f:
        f.write(yaml.safe_dump(params))


def read_json(path: str | Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def pick_file(initialdir: str = None, title="选择文件", types=[("所有文件", "*.*")]):
    if not initialdir:
        initialdir = Path.home()
    tk.Tk().withdraw()
    return filedialog.askopenfilename(
        initialdir=initialdir,
        title=title,
        filetypes=types,
    )


def pick_folder(initialdir: str = None, title="选择文件夹"):
    if not initialdir:
        initialdir = Path.home()
    tk.Tk().withdraw()
    return filedialog.askdirectory(
        title=title,
        initialdir=initialdir,
        mustexist=True,
    )
