try:
    str.removeprefix
except AttributeError:
    def removeprefix(value: str, prefix: str) -> str:
        return value[len(prefix):] if prefix and value.startswith(prefix) else value
else:
    def removeprefix(value: str, prefix: str) -> str:
        return value.removeprefix(prefix)

try:
    str.removesuffix
except AttributeError:
    def removesuffix(value: str, suffix: str) -> str:
        return value[:-len(suffix)] if suffix and value.endswith(suffix) else value
else:
    def removesuffix(value: str, suffix: str) -> str:
        return value.removesuffix(suffix)
