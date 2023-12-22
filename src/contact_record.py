import datetime
from src.utils.cli_parse_decorator import *
from src.utils.validator import is_valid_phone


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


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.address = []
        self.birthday = None

    def __str__(self):
        return (
            f"Contact name: {self.name.value}\n"
            f"phones: {', '.join(p.value for p in self.phones)}\n"
            f"emails: {', '.join(e.value for e in self.emails)}\n"
            f"address: {', '.join(a.value for a in self.address)}\n"
        )
    
    # Checks if the record field includes a value
    # Compitable with arrays and literal constants 
    #
    # e.g. record.field_has_value('emails', 'test@test.com')
    #
    # @params [String] field_name
    # @params [String] value
    # @return [Bool]
    def field_has_value(self, field_name, value):
        fields = getattr(self, field_name)

        if type(fields) is not list:
            fields = [fields]

        no_nones = [item for item in fields if item is not None]
        field_values = list(map(lambda field: field.value, no_nones))
        return value in field_values

    def add_phone(self, phone):
        if Phone.is_valid(phone):
            self.phones.append(Phone(phone))
        else:
            raise PhoneValueError

    def remove_phone(self, phone):
        self.phones.remove(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        if Phone.is_valid(new_phone):
            phone = self.find_item(old_phone, self.phones)
            if phone:
                phone.value = new_phone
            else:
                raise PhoneValueNotExist(self.name, old_phone)
        else:
            raise PhoneValueError

    def find_item(self, item, collection):
        return next((i for i in collection if i.value == item), None)

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_email(self, email):
        if Email.is_valid(email):
            self.emails.append(Email(email))
        else:
            raise EmailValueError(email)

    def edit_email(self, old_email, new_email):
        if Email.is_valid(new_email):
            email = self.find_item(old_email, self.emails)
            if email:
                email.value = new_email
            else:
                raise EmailValueNotExist(self.name, old_email)
        else:
            raise EmailValueError

    def remove_email(self, email):
        self.emails.remove(Email(email))

    def add_address(self, address):
        self.address.append(Address(address))

    def edit_address(self, old_address, new_address):
        address = self.find_item(old_address, self.address)
        if address:
            address.value = new_address
        else:
            raise AddressValueNotExist(self.name, old_address)

    def remove_address(self, address):
        self.address.remove(Address(address))
