from collections import UserDict
import os
import pickle

from src.utils.validator import is_valid_phone
from src.utils.cli_parse_decorator import *
from src.utils.dump_decorator import dump_contacts
from src.phone_book import *
from src.birthdays import get_birthdays_per_week
from src.contact_record import Record


@dump_contacts
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


@dump_contacts
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


@dump_contacts
@input_error
def change_contact(args, contacts):
    name = args[0]

    if name not in contacts:
        raise RecordDoesNotExistError(name)

    if len(args) == 3:
        if "@" in args[1] and "@" in args[2]:
            contacts[name].edit_email(args[1], args[2])
            return f"{name}'s email '{args[1]}' changed to '{args[2]}'."

        if args[1].isdigit() and args[2].isdigit():
            contacts[name].edit_phone(args[1], args[2])
            return f"{name}'s phone '{args[1]}' changed to '{args[2]}'."

    addresses = [
        x.strip() for x in " ".join(args[1:]).split(sep="|") if x != "" and x != " "
    ]
    if len(addresses) != 2:
        raise ValueError

    contacts[name].edit_address(addresses[0], addresses[1])
    return f"{name}'s address '{addresses[0]}' changed to '{addresses[1]}'."


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


@dump_contacts
@input_error
def add_birthday(args, contacts):
    name, date = args
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    contact.add_birthday(date)

    return "Birthday added."


@dump_contacts
@input_error
def add_email(args, contacts):
    name, email = args
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    contact.add_email(email)
    return "Email added."


@dump_contacts
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


def search(value, field_name, contacts):
    splitted_value = value.split(' ')
    search_result = (map(lambda v: contacts.search_by(field_name, v), splitted_value))

    return any(search_result)

def search_by_name(args, contacts):
    value = args[0]
    return search(value, 'name', contacts)
def search_by_birthday(args, contacts):
    value = args[0]
    return search(value, 'birthday', contacts)
def search_by_emails(args, contacts):
    value = args[0]
    return search(value, 'emails', contacts)
def search_by_phones(args, contacts):
    value = args[0]
    return search(value, 'phones', contacts)

class AddressBook(UserDict):
    def __init__(self, load_from_file=True):
        """
        Initialize an AddressBook instance.

        This constructor initializes an empty dictionary in the `data` attribute and
        loads data from a file into it if the file exists.
        """
        super().__init__()
        self.data = {}

        if load_from_file:
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
        
    def search_by(self, field_name, value):
        records = list(self.data.values())

        return list(filter(lambda record: record.field_has_value(field_name, value), records))

    def dump(self):
        """
        Serialize and save the data dictionary to a binary file using the Pickle format.
        The data is saved to the file "address_book.bin" in binary mode.
        :return: None
        """
        with open("./data/address_book.bin", "wb") as file:
            pickle.dump(self.data, file)

    def load(self):
        """
        Deserialize and load data from a binary file using the Pickle format.
        If the file "address_book.bin" exists, it loads the data from it into the AddressBook instance.
        :return:
        """
        FILENAME = "./data/address_book.bin"
        if os.path.exists(FILENAME):
            with open(FILENAME, "rb") as file:
                self.data = pickle.load(file)
