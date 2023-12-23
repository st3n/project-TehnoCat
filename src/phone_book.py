from collections import UserDict
import os
import pickle
from rich import print

from src.utils.validator import is_valid_phone
from src.utils.cli_parse_decorator import *
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

    @dump_contacts
    @input_error
    def add_contact(self, args):
        name, phone = args

        if name in self.data:
            self.data[name].add_phone(phone)
        else:
            record = Record(name)
            record.add_phone(phone)
            self.data.add_record(record)

        print(f"Phone number {phone} for contact {name} added.")

    @dump_contacts
    @input_error
    def remove_contact(self, args):
        if len(args) < 1:
            raise ValueError

        name = args[0]

        if len(args) == 1:
            self.delete(name)
            print(f"Contact {name} removed.")
            return

        if len(args) == 2:
            if "@" in args[1]:
                self.data[name].remove_email(args[1])
                print(f"{name}'s email '{args[1]}' removed.")
            elif args[1].isdigit():
                self.data[name].remove_phone(args[1])
                print(f"{name}'s phone '{args[1]}' removed.")
        else:
            full_address = " ".join(args[1:])
            self.data[name].remove_address(full_address)
            print(f"{name}'s address '{full_address}' removed.")

    @dump_contacts
    @input_error
    def change_contact(self, args):
        name = args[0]

        if name not in self.data:
            raise RecordDoesNotExistError(name)

        if len(args) == 3:
            if "@" in args[1] and "@" in args[2]:
                self.data[name].edit_email(args[1], args[2])
                print(f"{name}'s email '{args[1]}' changed to '{args[2]}'.")
                return
            elif args[1].isdigit() and args[2].isdigit():
                self.data[name].edit_phone(args[1], args[2])
                print(f"{name}'s phone '{args[1]}' changed to '{args[2]}'.")
                return

        addresses = [
            x.strip() for x in " ".join(args[1:]).split(sep="|") if x != "" and x != " "
        ]
        if len(addresses) != 2:
            raise ValueError

        self.data[name].edit_address(addresses[0], addresses[1])
        print(f"{name}'s address '{addresses[0]}' changed to '{addresses[1]}'.")

    @input_error
    def show_phone(self, args):
        if len(args) < 1:
            raise ValueError

        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(str(contact))

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
        name, date = args
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        self.data.add_birthday(date)
        print("Birthday added.")

    @dump_contacts
    @input_error
    def add_email(self, args):
        name, email = args
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        contact.add_email(email)
        print("Email added.")

    @dump_contacts
    @input_error
    def add_address(self, args):
        contact = self.find(args[0])
        if not contact:
            raise RecordDoesNotExistError

        contact.add_address(" ".join(args[1:]))
        print("Address added.")

    @input_error
    def show_birthday(self, args):
        if len(args) == 0:
            raise ValueError

        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(contact.birthday)

    @input_error
    def show_email(self, args):
        if len(args) == 0:
            raise ValueError
        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(contact.emails[0])

    @input_error
    def show_address(self, args):
        if len(args) == 0:
            raise ValueError
        name = args[0]
        contact = self.find(name)
        if not contact:
            raise RecordDoesNotExistError

        print(contact.address[0])

    def hello(self):
        print("[bold blue]How can I help you?[/bold blue]\U0001F600\n")

    def exit(self):
        print("[bold magenta]Goodbye![/bold magenta]\n\U0001FAE1")
        raise SystemExit(0)

    @input_error
    @input_error
    def show_birthdays_next_week(self):
        contacts_with_birthdays = list(
            filter(lambda name: self.find(name).birthday is not None, self.data)
        )
        print(
            get_birthdays_per_week(
                map(
                    lambda name: {
                        "name": name,
                        "birthday": self.find(name).birthday.value,
                    },
                    contacts_with_birthdays,
                )
            )
        )

    @input_error
    def show_birthdays_in_days(self, args):
        days_from_now = args[0]
        contacts_with_birthdays = list(
            filter(lambda name: self.find(name).birthday is not None, self.data)
        )
        print(
            get_birthdays_in_days(
                map(
                    lambda name: {
                        "name": name,
                        "birthday": self.find(name).birthday.value,
                    },
                    contacts_with_birthdays,
                ),
                int(days_from_now),
            )
        )

    def search(self, value, field_name):
        value = value.split(" ") if type(value) is str else [value]
        search_result = []

        for v in value:
            search_result += self.search_by(field_name, v)

        res = f"{len(search_result)} records found\n\n"
        res += "\n".join(list(map(lambda sr: str(sr), search_result)))
        return res

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
