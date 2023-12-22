from collections import UserDict
from utils.validator import is_valid_phone
from utils.cli_parse_decorator import *
from phone_book import *
from next_week_birthdays import get_birthdays_per_week
from record import Record
from consol import *
from rich.console import Console

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
        console = Console()
    return console.print(f"[bold purple]Phone number[/bold purple] {phone} [bold purple]for contact[/bold purple] [bold cyan]{name}[/bold cyan] [bold purple]added[/bold purple].\n")


@input_error
def change_contact(args, contacts):
    name, new_phone = args

    if not is_valid_phone(new_phone):
        raise PhoneValueError

    if name in contacts:
        record = contacts[name]
        # here could be more suitable logic
        record.phones[0].value = new_phone
        console = Console()
        return console.print(f"[bold purple]Contact [/bold purple][bold cyan]{name}[/bold cyan] [bold purple]new phone number is [/bold purple]{new_phone}.\n")
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
def show_all(args, contacts, console):
    if args:
        raise ValueError

    if not contacts:
        raise KeyError

    else:
        return display_table_all(contacts, console)


@input_error
def add_birthday(args, contacts):
    name, date = args
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    contact.add_birthday(date)
    console = Console()
    return console.print("[bold purple]Birthday added[/bold purple].\n")
                        


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


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
