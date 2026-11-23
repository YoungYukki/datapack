import questionary
from utils.store import STORE
from install import recipe


def main():
    generator = questionary.select(
        "选择生成器:",
        choices=STORE.STATIC.GENERATORS,
    ).ask()
    match generator:
        case "recipe":
            recipe()
        case _:
            print("没有选择生成器")
