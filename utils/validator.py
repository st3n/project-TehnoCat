import re


def is_valid_phone(phone: str) -> bool:
    return re.match(r"^\d{10}$", phone) is not None
