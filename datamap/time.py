from datetime import datetime


def parse_timestamp(value: int) -> datetime:
    if isinstance(value, int):
        try:
            return datetime.fromtimestamp(value)
        except (OSError, ValueError):
            return datetime.fromtimestamp(value / 1e3)
    return value
