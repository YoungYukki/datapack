import questionary
from install import main as install
from utils.sync import main as sync
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
        install()
    case "sync":
        sync()
    case "batch":
        batch()
    case _:
        pass
