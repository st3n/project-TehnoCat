from contact_data import *


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.address = []

    def __str__(self):
        return (
            f"Contact name: {self.name.value}\n"
            f"phones: {', '.join(p.value for p in self.phones)}\n"
            f"emails: {', '.join(e.value for e in self.emails)}\n"
            f"address: {', '.join(a.value for a in self.address)}\n"
        )

    def add_phone(self, phone):
        if Phone.is_valid(phone):
            self.phones.append(Phone(phone))
        else:
            raise PhoneValueError

    def remove_phone(self, phone):
        self.phones.remove(Phone(phone))

    def edit_phone(self, old_phone, new_phone):
        if Phone.is_valid_phone(new_phone):
            phone = self.find_phone(old_phone)
            if phone:
                phone.value = new_phone
            else:
                raise PhoneValueNotExist
        else:
            raise PhoneValueError

    def find_phone(self, phone):
        return next((item for item in self.phones if item.value == phone), None)

    def add_birthday(self, date):
        self.birthday = Birthday(date)

    def add_email(self, email):
        if Email.is_valid(email):
            self.emails.append(Email(email))
        else:
            raise EmailValueError(email)

    def remove_email(self, email):
        self.emails.remove(Email(email))

    def add_address(self, address):
        self.address.append(Address(address))

    def remove_address(self, address):
        self.address.remove(Address(address))
