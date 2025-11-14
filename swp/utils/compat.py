try:
    str.removesuffix
except AttributeError:
    def removesuffix(value: str, suffix: str) -> str:
        return value[:-len(suffix)] if suffix and value.endswith(suffix) else value
else:
    def removesuffix(value: str, suffix: str) -> str:
        return value.removesuffix(suffix)
