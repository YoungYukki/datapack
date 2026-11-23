import tkinter as tk
from tkinter import filedialog
from collections import Counter


def pick_file(title="选择文件", types=[("所有文件", "*.*")]):
    tk.Tk().withdraw()
    return filedialog.askopenfilename(title=title, filetypes=types)


def format_count(count: int) -> str:
    if count == 1:
        return ""
    return f"{count}"


def cut_minecraft(entry: str):
    return entry.replace("minecraft:", "")


def concat(joiner: str, iterable: list) -> str:
    result: dict = Counter(iterable)
    return joiner.join(
        f"{format_count(count)}{cut_minecraft(entry)}"
        for entry, count in result.items()
    )
