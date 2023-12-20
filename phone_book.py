from collections import UserDict
import os
import pickle

from utils.validator import is_valid_phone
from utils.cli_parse_decorator import *
from phone_book import *
from next_week_birthdays import get_birthdays_per_week
from record import Record


@input_error
def add_contact(args, contacts):
    name, phone = args

    if name in contacts:
        contacts[name].add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)

    return f"Phone number {phone} for contact {name} added."


@input_error
def remove_contact(args, contacts):
    if len(args) < 1:
        raise ValueError

    name = args[0]

    if len(args) == 1:
        contacts.delete(name)
        return f"Contact {name} removed."

    if len(args) == 2:
        if "@" in args[1]:
            contacts[name].remove_email(args[1])
            return f"{name}'s email '{args[1]}' removed."

        if args[1].isdigit():
            contacts[name].remove_phone(args[1])
            return f"{name}'s phone '{args[1]}' removed."
    else:
        full_address = " ".join(args[1:])
        contacts[name].remove_address(full_address)
        return f"{name}'s address '{full_address}' removed."


@input_error
def change_contact(args, contacts):
    name, old_phone, new_phone = args

    if name in contacts:
        contacts[name].edit_phone(old_phone, new_phone)
        return f"{old_phone} changed to {new_phone} for contact {name}"
    else:
        raise RecordDoesNotExistError(name)


@input_error
def show_phone(args, contacts):
    if len(args) < 1:
        raise ValueError

    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    return str(contact)


@input_error
def show_all(args, contacts):
    if args:
        raise ValueError

    if not contacts:
        raise KeyError

    prefix = "The phone book:\n"
    return prefix + "\n".join(map(lambda x: contacts.find(x).__str__(), contacts))


@input_error
def add_birthday(args, contacts):
    name, date = args
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    contact.add_birthday(date)
    return "Birthday added."


@input_error
def add_email(args, contacts):
    name, email = args
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    contact.add_email(email)
    return "Email added."


@input_error
def add_address(args, contacts):
    contact = contacts.find(args[0])
    if not contact:
        raise RecordDoesNotExistError

    contact.add_address(" ".join(args[1:]))
    return "Address added."


@input_error
def show_birthday(args, contacts):
    if len(args) == 0:
        raise ValueError

    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    return contact.birthday


@input_error
def show_email(args, contacts):
    if len(args) == 0:
        raise ValueError
    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    return contact.emails[0]


@input_error
def show_address(args, contacts):
    if len(args) == 0:
        raise ValueError
    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    return contact.address[0]


@input_error
def show_birthdays_next_week(_, contacts):
    return get_birthdays_per_week(
        map(
            lambda x: {"name": x, "birthday": contacts.find(x).birthday.value}, contacts
        )
    )


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.data = {}
        self.load()

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise RecordDoesNotExistError

    def dump(self):
        with open("address_book.bin", "wb") as file:
            pickle.dump(self.data, file)
        print("Saved to disk")

    def load(self):
        FILENAME = "address_book.bin"
        if os.path.exists(FILENAME):
            with open(FILENAME, "rb") as file:
                self.data = pickle.load(file)
