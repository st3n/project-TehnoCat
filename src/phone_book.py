from collections import UserDict
import os
import pickle
from rich import print
import datetime
from rich.console import Console

from utils.validator import is_valid_phone
from utils.cli_parse_decorator import *
from utils.dump_decorator import dump_contacts
from contact_record import Record
from consol import display_table_all
from birthdays import get_birthdays_per_week, get_birthdays_in_days


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

    return f"[bold purple]Phone number[/bold purple] {phone} [bold purple]for contact[/bold purple] [bold cyan]{name}[/bold cyan] [bold purple]added[/bold purple].\n"


@dump_contacts
@input_error
def remove_contact(args, contacts):
    if len(args) < 1:
        raise ValueError

    name = args[0]

    if len(args) == 1:
        contacts.delete(name)
        return f"[magenta]Contact[/magenta] [bold cyan]{name}[/bold cyan] [magenta]removed[/magenta].\n"

    if len(args) == 2:
        if "@" in args[1]:
            contacts[name].remove_email(args[1])
            return f"[bold cyan]{name}'s [/bold cyan][magenta]email[/magenta]'{args[1]}' [magenta]removed[/magenta].\n"

        if args[1].isdigit():
            contacts[name].remove_phone(args[1])
            return f"[bold cyan]{name}'s [/bold cyan][magenta]phone[/magenta] '{args[1]}' [magenta]removed[/magenta].\n"
    else:
        full_address = " ".join(args[1:])
        contacts[name].remove_address(full_address)
        return f"[bold cyan]{name}'s [/bold cyan][magenta]address[/magenta] '{full_address}' [magenta]removed[/magenta].\n"


@dump_contacts
@input_error
def change_contact(args, contacts):
    name = args[0]

    if name not in contacts:
        raise RecordDoesNotExistError(name)

    if len(args) == 3:
        if "@" in args[1] and "@" in args[2]:
            contacts[name].edit_email(args[1], args[2])
            return f"[bold cyan]{name}'s[/bold cyan] [bold purple]email '{args[1]}' changed to '{args[2]}'.\n"

        if args[1].isdigit() and args[2].isdigit():
            contacts[name].edit_phone(args[1], args[2])
            return f"[bold cyan]{name}'s[/bold cyan] [bold purple]phone [/bold purple]'{args[1]}'[bold purple] changed to[/bold purple] '{args[2]}'.\n"

    addresses = [
        x.strip() for x in " ".join(args[1:]).split(sep="|") if x != "" and x != " "
    ]
    if len(addresses) != 2:
        raise ValueError

    contacts[name].edit_address(addresses[0], addresses[1])
    return f"[bold cyan]{name}'s[/bold cyan] [bold purple]address[/bold purple] '{addresses[0]}' [bold purple]changed to [/bold purple]'{addresses[1]}'.\n"


@input_error
def show_contact(args, contacts):
    if len(args) < 1:
        raise ValueError

    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    return str(contact)



@input_error
def show_phone(args, contacts):
    if len(args) < 1:
        raise ValueError

    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    phones_str = ", ".join(str(phone.value) for phone in contact.phones) if contact.phones else "None"
    return phones_str + "\n"


@input_error
def show_all(args, contacts, console):
    if args:
        raise ValueError

    if not contacts.data:
        raise KeyError
    else:
        display_table_all(contacts)


@dump_contacts
@input_error
def add_birthday(args, contacts):
    name, date = args
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    contact.add_birthday(date)

    return "[bold purple]Birthday added[/bold purple].\n"


@dump_contacts
@input_error
def add_email(args, contacts):
    name, *emails = args
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    for email in emails:
        contact.add_email(email)

    return "[bold purple]Emails added[/bold purple].\n"


@dump_contacts
@input_error
def add_address(args, contacts):
    if len(args) < 2:
        raise ValueError

    name = args[0]
    address = " ".join(args[1:])
    
    contact = contacts.find(name)
    
    if contact:
        contact.add_address(address)
        return f"[bold cyan]{name}'s [/bold cyan][magenta]address[/magenta] '{address}' [magenta]added[/magenta].\n"
    else:
        raise RecordDoesNotExistError


@input_error
def show_birthday(args, contacts):
    if len(args) == 0:
        raise ValueError

    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError
    birthday_str = str(contact.birthday) if contact.birthday else "None"
    return birthday_str + "\n" 


@input_error
def show_email(args, contacts):
    if not args:
        raise ValueError("Name is required.")
    
    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError
    
    console = Console()

    if contact.emails:
        emails_str = "\n".join(f"[bold cyan]{email.value}[/bold cyan]" for email in contact.emails)
        console.print(emails_str + "\n")
    else:
        console.print("[bold cyan]None[/bold cyan]\n")
 
  
def show_address(args, contacts):
    if not args:
        raise ValueError("Name is required.")
    
    name = args[0]
    contact = contacts.find(name)
    if not contact:
        raise RecordDoesNotExistError

    console = Console()

    if contact.address:
        address_str = "\n".join(f"[bold cyan]{address.value}[/bold cyan]" for address in contact.address)
        console.print(address_str + "\n")
    else:
        console.print("[bold cyan]None[/bold cyan]\n")

@input_error
def show_birthdays_next_week(_, contacts):
    contacts_with_birthdays = list(
        filter(lambda name: contacts.find(name).birthday is not None, contacts)
    )
    return get_birthdays_per_week(
        map(
            lambda name: {"name": name, "birthday": contacts.find(name).birthday.value},
            contacts_with_birthdays,
        )
    )


def show_birthdays_in_days(args, contacts):
    days_from_now = args[0]
    contacts_with_birthdays = list(
        filter(lambda name: contacts.find(name).birthday is not None, contacts)
    )
    return get_birthdays_in_days(
        map(
            lambda name: {"name": name, "birthday": contacts.find(name).birthday.value},
            contacts_with_birthdays,
        ),
        int(days_from_now),
    )


def search(value, field_name, contacts):
    value = value.split(' ') if type(value) is str else [value]
    search_result = []
    
    for v in value:
        search_result += contacts.search_by(field_name, v)

    res = f"{len(search_result)} records found\n\n"
    res += "\n".join(list(map(lambda sr: str(sr), search_result)))
    return res


def search_by_name(args, contacts):
    value = args[0]
    return search(value, "name", contacts)


def search_by_birthday(args, contacts):
    value = datetime.datetime.strptime(args[0], "%d.%m.%Y")
    return search(value, 'birthday', contacts)

def search_by_emails(args, contacts):
    value = args[0]
    return search(value, "emails", contacts)


def search_by_phones(args, contacts):
    value = args[0]
    return search(value, "phones", contacts)


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
        return list(
            filter(lambda record: record.field_has_value(field_name, value), records)
        )

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
