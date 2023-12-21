import datetime
from utils.cli_parse_decorator import *
from utils.validator import is_valid_phone


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        if isinstance(other, Field):
            return self.value == other.value
        return False

    def __hash__(self):
        return hash(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Birthday(Field):
    def __init__(self, birthday):
        try:
            super().__init__(datetime.datetime.strptime(birthday, "%d.%m.%Y"))
        except ValueError:
            raise BirthdayValueError

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")


class Phone(Field):
    def __init__(self, phone):
        if not self.is_valid(phone):
            raise PhoneValueError
        super().__init__(phone)

    @staticmethod
    def is_valid(phone):
        return is_valid_phone(phone)


class Address(Field):
    def __init__(self, address):
        super().__init__(address)


class Email(Field):
    def __init__(self, email):
        if not self.is_valid(email):
            raise EmailValueError(email)
        super().__init__(email)

    @staticmethod
    def is_valid(email):
        return True  # TODO: should be implemented
