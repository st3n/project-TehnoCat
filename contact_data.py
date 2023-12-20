import datetime
from utils.cli_parse_decorator import *
from utils.validator import is_valid_phone


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    def is_eq(self, another_value):
        splitted_another_value = another_value.split(', ')
        arr_value = self.value
        if self.value is not list:
            arr_value = [self.value]
        
        return bool(set(arr_value).intersection(splitted_another_value))

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
        if not self.is_valid_phone(phone):
            raise ValueError("Error: The phone number must be 10 digits")
        super().__init__(phone)

    @staticmethod
    def is_valid_phone(phone):
        return is_valid_phone(phone)


class Email(Field):
    def __init__(self, email):
        if not self.is_valid_email(email):
            raise EmailValueError
        super().__init__(email)

    @staticmethod
    def is_valid_email(email):
        return is_valid_email(email)
