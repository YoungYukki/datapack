import questionary
from install import (
    datapack_install,
    datapack_sync,
)
from batch import main as batch
from utils import console

FUNCTIONS = [
    "install",
    "sync",
    "batch",
]

func = questionary.select("选择一项功能:", choices=FUNCTIONS).ask()
match func:
    case "install":
        datapack_install()
    case "sync":
        datapack_sync()
    case "batch":
        batch()
    case _:
        pass
