# 颜色定义
RESET = "\033[0m"
COLORS = {
    "info": "\033[94m",  # 亮蓝色
    "success": "\033[92m",  # 亮绿色
    "warning": "\033[93m",  # 亮黄色
    "danger": "\033[91m",  # 亮红色
}


def _log(level: str, message: str) -> None:
    """内部统一输出函数"""
    label = level.upper()
    color = COLORS[level]
    print(f"{color}[{label}]\n - {message}{RESET}")


def info(message: str) -> None:
    _log("info", message)


def success(message: str) -> None:
    _log("success", message)


def warning(message: str) -> None:
    _log("warning", message)


def danger(message: str) -> None:
    _log("danger", message)
