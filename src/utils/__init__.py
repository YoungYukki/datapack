from collections import Counter


def format_count(count: int) -> str:
    if count == 1:
        return ""
    return f"{count}"


def cut_minecraft(entry: str):
    sep = "minecraft:"
    _, found, rest = entry.partition(sep)
    if found == '':
        return entry
    return rest


def concat(joiner: str, iterable: list) -> str:
    result: dict = Counter(iterable)
    print(result)
    return joiner.join(
        f"{format_count(count)}{cut_minecraft(entry)}" for entry, count in result.items()
    )
