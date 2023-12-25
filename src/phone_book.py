from collections import UserDict
import os
import pickle
from rich import print
import datetime
import re

from src.utils.validator import is_valid_phone
from src.utils.cli_parse_decorator import *
from src.utils.demo_data import generate_fake_contacts_data
from src.utils.dump_decorator import dump_contacts
from src.phone_book import *
from src.birthdays import *
from src.contact_record import Record
from src.consol import ConsolePrinter


class PhoneBook(UserDict):
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

        self.console = ConsolePrinter(self)

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

    def import_demo(self):
        for contact_info in generate_fake_contacts_data(10):
            self.add_contact({"name" : contact_info["name"], "phone" : contact_info["phone"]})
            self.add_birthday({"name" :contact_info["name"], "birthday": contact_info["birthday"]})
            self.add_email({"name" : contact_info["name"], "email": contact_info["email"]})
            self.add_address({"name" :contact_info["name"], "address" : contact_info["address"]})

        return "Demo data has been imported successfully"

    def get_contact(self, args, args_expected_size: int):
        if len(args) < args_expected_size:
            raise ValueError

        contact = self.find(args[0])
        if not contact:
            raise RecordDoesNotExistError

        return contact

    @dump_contacts
    @input_error
    def add_contact(self, args):
        name = args["name"]
        if name in self.data:
            raise RecordAlreadyExistsError

        record = Record(name)
        self.add_record(record)
        if args["phone"]:
            self.add_phone(args)
        if args["email"]:
            self.add_email(args)
        if args["address"]:
            self.add_address(args)

        return f"[bold purple]Ccontact[/bold purple] [bold cyan]{name}[/bold cyan] [bold purple]added[/bold purple].\n"

    @dump_contacts
    @input_error
    def remove_contact(self, name):
        self.delete(name)
        print(f"[magenta]Contact[/magenta] [bold cyan]{name}[/bold cyan] [magenta]removed[/magenta].\n")

    @dump_contacts
    @input_error
    def remove_phone(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].remove_phone(args["phone"])
        print(f"[bold cyan]{name}'s [/bold cyan][magenta]phone[/magenta] '{args["phone"]}' [magenta]removed[/magenta].\n")

    @dump_contacts
    @input_error
    def remove_email(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].remove_email(args["email"])
        print(f"[bold cyan]{name}'s [/bold cyan][magenta]email[/magenta]'{args["email"]}' [magenta]removed[/magenta].\n")

    @dump_contacts
    @input_error
    def remove_address(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].remove_address(args["address"])
        print(f"[bold cyan]{name}'s [/bold cyan][magenta]address[/magenta] '{args["address"]}' [magenta]removed[/magenta].\n")

    @dump_contacts
    @input_error
    def change_phone(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].edit_phone(args["old_value"], args["new_value"])
        print(f"[bold cyan]{name}'s[/bold cyan] [bold purple]phone [/bold purple]'{args["old_value"]}'[bold purple] changed to[/bold purple] '{args["new_value"]}'.\n")

    @dump_contacts
    @input_error
    def change_email(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].edit_email(args["old_value"], args["new_value"])
        print(f"[bold cyan]{name}'s[/bold cyan] [bold purple]email '{args["old_value"]}' changed to '{args["new_value"]}'.\n")

    @dump_contacts
    @input_error
    def change_address(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].edit_address(args["old_value"], args["new_value"])
        print(f"[bold cyan]{name}'s[/bold cyan] [bold purple]address[/bold purple] '{args["old_value"]}' [bold purple]changed to [/bold purple]'{args["new_value"]}'.\n")

    @input_error
    def show_contact(self, args):
        if len(args) < 1:
            raise ValueError

        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(str(contact))

    @input_error
    def add_phone(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].add_phone(args["phone"])
        print("[bold purple]Phone added[/bold purple].\n")

    @input_error
    def show_phone(self, args):
        if len(args) < 1:
            raise ValueError

        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(
            ", ".join(str(p.value) for p in contact.phones)
            if contact.phones
            else "None"
        )

    @input_error
    def show_all(self):
        if not self.data:
            raise KeyError

        self.console.display_table_all()

    def show_help(self):
        self.console.display_help()

    @dump_contacts
    @input_error
    def add_birthday(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[args["name"]].add_birthday(args["birthday"])
        print("[bold purple]Birthday added[/bold purple].\n")

    @dump_contacts
    @input_error
    def add_email(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].add_email(args["email"])
        print("[bold purple]Email added[/bold purple].\n")

    @dump_contacts
    @input_error
    def add_address(self, args):
        name = args["name"]
        if name not in self.data:
            raise RecordDoesNotExistError

        self.data[name].add_address(args["address"])
        print(
            f"[bold cyan]{name}'s [/bold cyan][magenta]address[/magenta] '{args["address"]}' [magenta]added[/magenta].\n"
        )

    @input_error
    def show_birthday(self, args):
        if len(args) == 0:
            raise ValueError

        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(str(contact.birthday) if contact.birthday else "None")

    @input_error
    def show_email(self, args):
        if len(args) == 0:
            raise ValueError
        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(
            ", ".join(str(p.value) for p in contact.emails)
            if contact.emails
            else "None"
        )

    @input_error
    def show_address(self, args):
        if len(args) == 0:
            raise ValueError
        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        address_str = "\n".join(
            f"[bold cyan]{address.value}[/bold cyan]" for address in contact.address
        )
        self.console.display_address(address_str)

    def hello(self):
        print("[bold blue]How can I help you?[/bold blue]\U0001F600\n")

    def exit(self):
        print("[bold magenta]Goodbye![/bold magenta]\n\U0001FAE1")
        raise SystemExit(0)

    @input_error
    def show_birthdays_next_week(self):
        contacts_with_birthdays = list(
            filter(lambda name: self.find(name).birthday is not None, self.data)
        )
        birthdays_per_week = birthdays_per_week(
            map(
                lambda name: {
                    "name": name,
                    "birthday": self.find(name).birthday.value,
                },
                contacts_with_birthdays,
            )
        )

        self.console.display_birthdays_next_week(birthdays_per_week)

    @input_error
    def show_birthdays_in_days(self, args):
        days_from_now = args[0]
        contacts_with_birthdays = list(
            filter(lambda name: self.find(name).birthday is not None, self.data)
        )
        data = get_birthdays_in_days(
            map(
                lambda name: {
                    "name": name,
                    "birthday": self.find(name).birthday.value,
                },
                contacts_with_birthdays,
            ),
            int(days_from_now),
        )
        self.console.display_birthdays_in_days(data)

    def search(self, value, field_name):
        value = re.split(r"\n|\s", value) if type(value) is str else [value]
        search_result = []

        for v in value:
            search_result += self.search_by(field_name, v)

        print(f"{len(search_result)} records found:")
        res = [(rec.name.value, rec) for rec in search_result]
        self.console.display_table(res)

    def search_by(self, field_name, value):
        records = list(self.data.values())
        return list(
            filter(lambda record: record.field_has_value(field_name, value), records)
        )

    def search_by_name(self, args):
        value = args[0]
        return self.search(value, "name")

    def search_by_birthday(self, args):
        value = datetime.datetime.strptime(args[0], "%d.%m.%Y")
        return self.search(value, "birthday")

    def search_by_emails(self, args):
        value = args[0]
        return self.search(value, "emails")

    def search_by_phones(self, args):
        value = args[0]
        return self.search(value, "phones")

    @dump_contacts
    @input_error
    def add_note(self, args):
        [name] = args
        contact = self.find(name)
        if not contact:
            record = Record(name)
            self.add_record(record)

        contact = self.find(name)
        contact.add_note()
        return "Notes added."

    @dump_contacts
    @input_error
    def edit_note(self, args):
        [name] = args
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        contact.edit_note()
        return "Notes edited."

    def search_by_note(self, args):
        value = args[0]
        return self.search(value, "notes")

    def search_by_tag(self, args):
        value = args[0]
        return self.search(value, "notes_tags")
