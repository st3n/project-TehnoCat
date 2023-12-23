import re


def is_valid_phone(phone: str) -> bool:
    return re.match(r"^\d{10}$", phone) is not None


def is_valid_email(email: str) -> bool:
    return bool(re.match(r"[A-Za-z]+[A-Za-z0-9_\.]+@[A-Za-z]{2,}\.[A-Za-z]{2,}", email))
