from collections import UserDict
from utils.validator import is_valid_phone
from utils.cli_parse_decorator import *
from phone_book import *
from next_week_birthdays import get_birthdays_per_week
from record import Record


@input_error
def add_contact(args, contacts):
    name, phone = args

    if not is_valid_phone(phone):
        raise PhoneValueError

    if name in contacts:
        contacts[name].add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)

    return f"Phone number {phone} for contact {name} added."


@input_error
def change_contact(args, contacts):
    name, new_phone = args

    if not is_valid_phone(new_phone):
        raise PhoneValueError

    if name in contacts:
        record = contacts[name]
        # here could be more suitable logic
        record.phones[0].value = new_phone
        return f"Contact {name} new phone number is {new_phone}."
    else:
        raise RecordDoesNotExistError


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
def show_birthday(args, contacts):
    if len(args) == 0:
        raise ValueError

    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    return contact.birthday


def show_birthdays_next_week(contacts):
    return get_birthdays_per_week(
        map(
            lambda x: {"name": x, "birthday": contacts.find(x).birthday.value}, contacts
        )
    )


def search(args, command, contacts):
    value = args[0]
    criteria = command.split('-')[-1]
    return contacts.search_by(criteria, value)


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)
    
    def search_by(self, criteria, value):
        records = list(self.data.values())
        def is_field_eq(record):
            return getattr(record, criteria).value_includes(value)
        
        return list(filter(lambda record: is_field_eq(record), records))

    def delete(self, name):
        if name in self.data:
            del self.data[name]
